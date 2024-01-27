from django.urls import include, path
from rest_framework.routers import SimpleRouter

from ._views import *
from .views import *

app_name='user'

view_customuser = SimpleRouter()
view_customuser.register('', CustomUserView, basename='user-router')

rescue_password = SimpleRouter()
rescue_password.register('rescue_password', RescuePasswordViewSet, basename='rescue_password')

change_password = SimpleRouter()
change_password.register('change_password', ChangePasswordViewSet, basename='change_password')

urlpatterns = [
    path('login/', CustomUserView.as_view({'post': 'login'}), name='user-login'),
    path('logout/<uuid:pk>/', CustomUserView.as_view({'post': 'logout'}), name='user-logout'),
    path('', include(view_customuser.urls)),
    path('before_login/', include(rescue_password.urls)),
    path('rescue_password/<str:email>/', RescuePasswordViewSet.as_view({'patch': 'partial_update'}), name='rescue_password_detail'),
    path('rescue_password/<str:email>/change/', RescuePasswordViewSet.as_view({'delete': 'change_password'}), name='rescue_password_delete'),
    path('by_settings/', include(change_password.urls)),
    path('change_password/', ChangePasswordViewSet.as_view({'delete': 'change_password'}), name='change_password_delete'),
]
