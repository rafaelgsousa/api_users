import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.urls import resolve
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

        except json.JSONDecodeError as e:
            logger.error(f'Error decoding request JSON: {e}')
            return JsonResponse({'error': 'Invalid JSON format in request body.'}, status=400)

        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            return JsonResponse({'error': 'Unexpected error'}, status=500)

        return response

    def extract_request_data(self, request, response, request_body):
        user_id = None
        email = ''
        body = None
        view_name = ''

        user_id = request.user.id if request.user else None
        
        if not user_id and isinstance(response, Response):
            user_id = get_value_for_key(response.data, 'id')
            email = get_value_for_key(response.data, 'email') if not user_id else None

        if not user_id and not email and isinstance(response, Response):
            user_id = get_value_for_key(request.resolver_match.kwargs, 'pk')
            email = get_value_for_key(request.resolver_match.kwargs, 'email')
            email = get_value_for_key(json.loads(request_body.decode('utf-8')), 'email') if not email and len(request_body.decode('utf-8')) else email

        if not user_id and not email and isinstance(response, JsonResponse):
            user_id = get_value_for_key(resolve(request.path).kwargs,'pk')
            email = get_value_for_key(resolve(request.path).kwargs,'email') if not user_id else None

        if hasattr(request, 'resolver_match') and request.resolver_match:
            view_name = request.resolver_match.url_name

        if request.method == 'POST' and 'logout' in request.path:
            body = None
        else:
            if request_body:
                body = json.loads(request_body.decode('utf-8'))

        return user_id, email, body, view_name

    def log_request_data(self, request, user_id, email, body, view_name, response):
        try:
            user = None

            if user_id:
                user = CustomUser.objects.filter(id=user_id).first()

            if not user and email:
                user = CustomUser.objects.filter(email=email).first()

            if user:
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
            else:
                logger.error('User not found.')
                return JsonResponse({'error': 'User not found.'}, status=404)
        except ObjectDoesNotExist:
            logger.error('User not found.')
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            logger.error(f'Error getting user: {e}')
            return JsonResponse({'error': 'Error getting user.'}, status=500)
