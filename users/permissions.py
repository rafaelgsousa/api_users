from django.apps import apps
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import *


class IsOwnerOrLevelRequired(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id is None:
            return False
        user_req = CustomUser.objects.get(id=request.user.id)
        if user_req.id != obj.id and view.action in ['partial_update', 'destroy']:
            return user_req.nv_user > obj.nv_user
        if user_req.id != obj.id and view.action in ['retrieve']:
            return user_req.nv_user > 0
        return True
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
class LevelHigher(BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.user.id is None:
            return False
        return super().has_object_permission(request,view,obj)
    
    def has_permission(self, request, view):
        user_req = CustomUser.objects.get(id=request.user.id)
        return user_req.nv_user > 0

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id is None:
            return False
        user_req = CustomUser.objects.get(id=request.user.id)
        return user_req.id != obj.id
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)


def switch(case):
    if case == 'POST':
        return 'add'
    elif case == 'GET':
        return 'view'
    elif case == 'PATCH':
        return 'change'
    elif case == 'DELETE':
        return 'delete'
    else:
        return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)


class CheckPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request,view,obj)
    
    def has_permission(self, request, view):
        app_label = view.__module__.split('.')[0]
        app_name = apps.get_app_config(app_label).verbose_name.lower()
        request_method = request.method
        name_method = switch(request_method)
        model_lower = view.queryset.model.__name__.lower()
        group_permissions = request.user.get_group_permissions()
        permission_to_check = f'{app_name}.{name_method}_{model_lower}'
        return permission_to_check in group_permissions