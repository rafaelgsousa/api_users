from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from .models import *


class IsOwnerOrLevelRequired(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_req = get_object_or_404(CustomUser, id=request.user.id)
        if user_req.id != obj.id and view.action in ['partial_update', 'destroy']:
            return user_req.nv_user > obj.nv_user
        if user_req.id != obj.id and view.action in ['retrieve']:
            return user_req.nv_user > 0
        return True
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
class LevelHigher(BasePermission):
    def has_object_permission(self,request,view,obj):
        
        return super().has_object_permission(request,view,obj)
    
    def has_permission(self, request, view):
        user_req = get_object_or_404(CustomUser, id=request.user.id)
        return user_req.nv_user > 0

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_req = get_object_or_404(CustomUser, id=request.user.id)
        return user_req.id != obj.id
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)