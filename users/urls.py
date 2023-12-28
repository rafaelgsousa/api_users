from django.urls import path

from .views import *

app_name='user'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/<uuid:id>/', logout, name='logout'),
    path('change_password/', change_password_by_settings, name='change_password_by_setting'),
    path('change_password/', change_password_by_login_page, name='change_password_by_login_page'),
    path('<uuid:id>/', get_user, name='get_user'),
    path('list/', get_users, name='get_users'),
    path('update_user/<uuid:id>/', update_user, name='update_user'),
    # path('inactive_user/<uuid:id>/', inactive_user, name='inactive_user'),
    path('delete_user/<uuid:id>/', delete_user, name='delete_user'),
]