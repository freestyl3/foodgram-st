from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author

class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.method in SAFE_METHODS