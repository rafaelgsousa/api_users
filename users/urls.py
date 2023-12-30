from django.urls import path

from .views import *

app_name='user'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('send_code/<str:email>/', send_verification_code_before_login, name='send_verification_code_before_login'),
    path('verify_code/', verify_code_before_login, name='verify_code_before_login'),
    path('change_password/<str:email>', change_password_before_login, name='change_password_before_login'),
    path('send_code/settings/', send_verification_code_by_settings, name='send_verification_code_by_settings'),
    path('verify_code/settings/', verify_code_by_settings, name='verify_code_by_settings'),
    path('change_password/settings', change_password_by_settings, name='change_password_by_setting'),
    path('logout/<uuid:id>/', logout, name='logout'),
    path('<uuid:id>/', get_user, name='get_user'),
    path('list/', get_users, name='get_users'),
    path('update_user/<uuid:id>/', update_user, name='update_user'),
    path('delete_user/<uuid:id>/', delete_user, name='delete_user'),
]