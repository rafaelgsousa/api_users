from django.urls import path

from .views import *

app_name='user'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/<uuid:id>/', logout, name='logout'),
    path('change_password/settings', change_password_by_settings, name='change_password_by_setting'),
    path('send_email/forget_password/', forget_password_send_email, name='forget_password_send_email'),
    path('change_password/login', change_password_by_login_page, name='change_password_by_login_page'),
    path('<uuid:id>/', get_user, name='get_user'),
    path('list/', get_users, name='get_users'),
    path('update_user/<uuid:id>/', update_user, name='update_user'),
    path('delete_user/<uuid:id>/', delete_user, name='delete_user'),
]