import json
import logging

from ..models import CustomUser, Logger

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Armazena o corpo da requisição antes de verificar se é uma requisição de logout
            request_body = request.body
            response = self.get_response(request)

            if request.method == 'POST' and 'logout' in request.path:
                # Evite decodificar o corpo para requisições de logout
                body = None
            else:
                body = json.loads(request_body.decode('utf-8')) if request_body else None

            # Restante do seu código...
        except CustomUser.DoesNotExist as user_not_found_error:
            logger.error(f'Erro ao obter usuário: {user_not_found_error}')
        except json.JSONDecodeError as json_decode_error:
            logger.error(f'Erro ao decodificar JSON: {json_decode_error}')
        except Exception as e:
            logger.error(f'Erro inesperado: {e}')

        return response

