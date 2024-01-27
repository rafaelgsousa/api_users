import json

from django.core.exceptions import BadRequest, PermissionDenied
from django.http import JsonResponse

FORBIDDEN_KEYS = ['is_logged_in', 'password', 'login_erro', 'id', 'update_at', 'created_at', 'last_login_sistem']

class CheckBodyRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            self.check_request_body(request)
            self.check_forbidden_keys(request)
            response = self.get_response(request)
            return response
        except (BadRequest) as e:
            return JsonResponse({'error': str(e)}, status=400)
        except (PermissionDenied) as e:
            return JsonResponse({'error': str(e)}, status=401)

    def check_request_body(self, request):
        if request.method == 'PATCH' and not request.body:
            raise BadRequest('Request body cannot be None.')

    def check_forbidden_keys(self, request):
        if request.method == 'PATCH' and request.body:
            try:
                request_data = json.loads(request.body.decode('utf-8'))
                if any(item in request_data.keys() for item in FORBIDDEN_KEYS):
                    raise PermissionDenied('No authorization for this procedure.')
            except json.JSONDecodeError:
                raise BadRequest('Invalid JSON format in request body.')
