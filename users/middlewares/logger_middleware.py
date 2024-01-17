import json
from copy import deepcopy

from ..models import CustomUser, Logger


class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            body = json.loads(request.body.decode('utf-8')) if request.body.decode('utf-8') else None
            
            response = self.get_response(request)

            if request.auth:
                id = request.auth['user_id']
                user = CustomUser.objects.get(id=id)
            else:
                id= json.loads(response.content.decode('utf-8'))['user']['id']
                user = CustomUser.objects.get(id=id)

            if body != None and 'password' in body:
                del body['password']

            Logger.objects.create(
                endpoint=request.path,
                user=user,
                method=request.method,
                body= str(body),
                view=request.resolver_match.url_name,
                status=response.status_code,
            )
        except CustomUser.DoesNotExist as user_not_found_error:
            print(f'Erro ao obter usuário: {user_not_found_error}')
        except json.JSONDecodeError as json_decode_error:
            print(f'Erro ao decodificar JSON: {json_decode_error}')
        except Exception as e:
            print(f'Erro inesperado: {e}')

        return response