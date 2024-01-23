from django.urls import include, path
from rest_framework.routers import SimpleRouter

from ._views import *
from .views import *

app_name='user'

view_customuser = SimpleRouter()
view_customuser.register('', CustomUserView, basename='user-router')

view_change_password_before_login = SimpleRouter()
view_change_password_before_login.register('change_password_before_login', CodeBeforeLogin, basename='change_password_before_login')

view_change_password_by_settings = SimpleRouter()
view_change_password_by_settings.register('change_password_by_settings', CodeBySettings, basename='change_password_by_settings')

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('send_code/<str:email>/', send_verification_code_before_login, name='send_verification_code_before_login'),
    path('verify_code/', verify_code_before_login, name='verify_code_before_login'),
    path('change_password/<str:email>/', change_password_before_login, name='change_password_before_login'),
    path('settings/send_code/', send_verification_code_by_settings, name='send_verification_code_by_settings'),
    path('settings/verify_code/', verify_code_by_settings, name='verify_code_by_settings'),
    path('settings/change_password/', change_password_by_settings, name='change_password_by_setting'),
    path('logout/<uuid:id>/', logout, name='logout'),
    path('user/<uuid:id>/', get_user, name='get_user'),
    path('users/', get_users, name='get_users'),
    path('update_user/<uuid:id>/', update_user, name='update_user'),
    path('delete_user/<uuid:id>/', delete_user, name='delete_user'),
    path('', include(view_customuser.urls)),
    path('', include(view_change_password_before_login.urls)),
    path('', include(view_change_password_by_settings.urls))
]