import json

from django.core.exceptions import BadRequest, PermissionDenied
from django.http import JsonResponse


class CheckBodyRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            forbidden_keys = ['is_logged_in', 'password', 'login_erro', 'id', 'update_at', 'created_at', 'last_login_sistem']
            
            if request.body and request.method == 'PATCH' and any(item in json.loads(request.body.decode('utf-8')).keys() for item in forbidden_keys):
                raise PermissionDenied('No authorization for this procedure.')
            if request.method == 'PATCH' and not request.body:
                raise BadRequest('Request body cannot be None.')
            response = self.get_response(request)
            
            return response
        except PermissionDenied as e:
            return JsonResponse({'error': str(e)}, status=401)
        except BadRequest as e:
            return JsonResponse({'error': str(e)}, status=400)