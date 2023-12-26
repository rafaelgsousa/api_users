from rest_framework import status
from rest_framework.response import Response


def check_level(user_act, bar):
    if user_act.nv_user < bar:
        return Response(
            {
                'error': 'Unauthorized',
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
def check_levels(user_act, user_pass):
    if user_act.nv_user < user_pass.nv_user:
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
    

def check_level_to_update_nv_user(body, user_act, user_pass):
    if (len(body) > 1 or 'nv_user' not in body or user_act.nv_user < 1 or 
        user_pass.nv_user >= user_act.nv_user or body['nv_user'] > user_act.nv_user):
        return Response(
            {
                'error': 'Unauthorized',
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

