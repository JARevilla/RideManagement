from rest_framework import permissions # type: ignore

class IsAPIAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'ADMIN'
