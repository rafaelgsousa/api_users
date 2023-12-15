from django.urls import path

from .views import *

app_name='user'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('get_user/', get_user, name='get_user'),
    path('get_users/', get_users, name='get_users'),
    path('update_user/', update_user, name='update_user'),
    path('inactive_user/', inactive_user, name='inactive_user'),
    path('delete_user/', delete_user, name='delete_user'),
]