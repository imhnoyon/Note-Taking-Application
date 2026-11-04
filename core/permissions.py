from rest_framework.permissions import BasePermission
from .models import User


class IsAdminRole(BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )


class IsUserRole(BasePermission):
    """
    Allows access to users with the 'user' role.
    """
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.USER
        )

