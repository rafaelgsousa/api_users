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
        except (BadRequest, PermissionDenied) as e:
            return JsonResponse({'error': str(e)}, status=self.get_status_code(e))
        
        return self.get_response(request)

    def get_status_code(self, exception):
        if isinstance(exception, BadRequest):
            return 400
        elif isinstance(exception, PermissionDenied):
            return 403
        return 500

    def check_request_body(self, request):
        if request.method == 'PATCH' and not request.body:
            raise BadRequest('The request body cannot be empty.')

    def check_forbidden_keys(self, request):
        if request.method == 'PATCH' and request.body:
            try:
                request_data = json.loads(request.body)
                if any(key in request_data for key in FORBIDDEN_KEYS):
                    raise PermissionDenied('No authorization for this procedure.')
            except json.JSONDecodeError:
                raise BadRequest('Invalid JSON format in the request body.')
