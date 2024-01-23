from rest_framework.permissions import BasePermission

class IsOwnerOrLevelHigher(BasePermission):
    def has_object_permission(self,request,view,obj):
        return True
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)