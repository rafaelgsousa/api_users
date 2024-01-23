import json
import logging

from ..models import CustomUser, Logger

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)

            if request.method == 'POST' and 'logout' in request.path:
                # Evite decodificar o corpo para requisições de logout
                body = None
            else:
                body = json.loads(request.body.decode('utf-8')) if request.body else None

            user_id = None

            if request.auth:
                user_id = request.auth['user_id']
            elif response.content:
                user_id = json.loads(response.content.decode('utf-8')).get('user', {}).get('id')

            if user_id:
                user = CustomUser.objects.get(id=user_id)

                if body and 'password' in body:
                    del body['password']

                Logger.objects.create(
                    endpoint=request.path,
                    user=user,
                    method=request.method,
                    body=str(body),
                    view=request.resolver_match.url_name,
                    status=response.status_code,
                )
        except CustomUser.DoesNotExist as user_not_found_error:
            logger.error(f'Erro ao obter usuário: {user_not_found_error}')
        except json.JSONDecodeError as json_decode_error:
            logger.error(f'Erro ao decodificar JSON: {json_decode_error}')
        except Exception as e:
            logger.error(f'Erro inesperado: {e}')

        return response
