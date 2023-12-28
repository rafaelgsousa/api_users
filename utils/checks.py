from rest_framework.exceptions import PermissionDenied


def check_level(user_act, bar):
    if user_act.nv_user < bar:
        raise PermissionDenied(detail='Permission denied: nv_user insufficient.')
    
def check_levels(user_act, user_pass):
    if user_act.nv_user < user_pass.nv_user:
        raise PermissionDenied(detail='Permission denied: nv_user insufficient.')
    
def check_level_to_update_nv_user(body, user_act, user_pass):
    if ('nv_user' in body) and (user_act.nv_user < 1 or 
        user_pass.nv_user >= user_act.nv_user or body['nv_user'] > user_act.nv_user):
        raise PermissionDenied(detail='Permission denied: Update not permitted for nv_user.')
    
    if ('is_active' in body) and (user_act.nv_user < 1 or 
        user_pass.nv_user >= user_act.nv_user):
        raise PermissionDenied(detail='Permission denied: Update not permitted for is_active.')
    
def check_update_is_logged_in(body):
    if 'is_logged_in' in body:
        raise PermissionDenied(detail='Permission denied: Update not permitted for is_logged_in.')
