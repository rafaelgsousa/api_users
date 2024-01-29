import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response

from utils import get_value_for_key

from ..models import CustomUser, Logger

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request_body = request.body
            response = self.get_response(request)

            user_id, email, body, view_name = self.extract_request_data(request, response, request_body)
            self.log_request_data(request, user_id, email, body, view_name, response)

        except Exception as e:
            logger.error(f'Erro inesperado: {e}')
            return JsonResponse({'error': 'Erro inesperado'}, status=500)

        return response

    def extract_request_data(self, request, response, request_body):
        user_id = None
        email = ''
        body = None
        view_name = ''

        # Casos com rotas que usam token
        user_id = request.user.id if request.user else None
        
        if not user_id and isinstance(response, Response):
            # Casos de login e register
            user_id = get_value_for_key(response.data, 'id')
            email = get_value_for_key(response.data, 'email') if not user_id else None
        # if not user_id and not email:
        #     # Casos de rescue password
        #     user_id = request.GET.get('id', None)
        #     # print(f'user_id {user_id}')
        #     email = request.GET.get('email', None) if not user_id else None
        #     # print(f'email1 {email}')
        #     email = json.loads(request_body.decode('utf-8'))['email'] if not email and 'email' in json.loads(request_body.decode('utf-8')).keys() else email
        #     # print(f'email2 {email}')

        if not user_id and not email and isinstance(response, JsonResponse):
            # Casos onde o body do patch será errado e pare no middleware
            user_id = get_value_for_key(json.loads(response.content.decode('utf-8')), 'id')
            email = get_value_for_key(json.loads(response.content.decode('utf-8')), 'email') if not user_id else None

        if hasattr(request, 'resolver_match') and request.resolver_match:
            view_name = request.resolver_match.url_name

        if request.method == 'POST' and 'logout' in request.path:
            body = None
        else:
            if request_body:
                try:
                    body = json.loads(request_body.decode('utf-8'))
                except json.JSONDecodeError as e:
                    logger.error(f'Erro ao decodificar JSON da requisição: {e}')

        return user_id, email, body, view_name

    def log_request_data(self, request, user_id, email, body, view_name, response):
        try:
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                if body and 'password' in body:
                    del body['password']

                Logger.objects.create(
                    endpoint=request.path,
                    user=user,
                    method=request.method,
                    body=str(body),
                    view=view_name,
                    status=response.status_code,
                )

            if not user_id and email:
                user = CustomUser.objects.get(email=email)
                if body and 'password' in body:
                    del body['password']

                Logger.objects.create(
                    endpoint=request.path,
                    user=user,
                    method=request.method,
                    body=str(body),
                    view=view_name,
                    status=response.status_code,
                )
        except ObjectDoesNotExist as e:
            logger.error(f'Erro ao obter usuário: {e}')
