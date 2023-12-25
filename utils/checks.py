from rest_framework import status
from rest_framework.response import Response


def check_level(user, required_lv):
    if user.nv_user < required_lv:
        return Response(
            {
                'error': 'Unauthorized',
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
def check_logged_in(user):
    if not user.is_logged_in:
        return Response(
            {
                'error': 'User not logged in'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )