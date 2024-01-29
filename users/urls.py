from django.urls import include, path
from rest_framework.routers import SimpleRouter

from ._views import *
from .views import *

app_name='user'

view_customuser = SimpleRouter()
view_customuser.register('', CustomUserView, basename='user-router')

rescue_password = SimpleRouter()
rescue_password.register(r'rescue_password/before_login', RescuePasswordViewSet, basename='rescue_password')

change_password = SimpleRouter()
change_password.register(r'change_password/settings', ChangePasswordViewSet, basename='change_password')

urlpatterns = [
    path('', include(view_customuser.urls)),
    path('', include(rescue_password.urls)),
    path('', include(change_password.urls)),
]
