from . import exceptions
from rest_framework.permissions import BasePermissionMetaclass
from rest_framework.permissions import SAFE_METHODS


class IsSuperUserOrReadOnly(metaclass=BasePermissionMetaclass):
    """
    ReadOnly Allowed for Everyone
    NOT IN SAFE METHODS ONLY SUPERUSER
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationRequired()
        if request.user.is_superuser == True:
            return True
        return False

        # raise exceptions.PermissionDenied()

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationRequired()
        if request.user.is_superuser == True:
            return True
        return False
        # raise exceptions.PermissionDenied()



__all__ = [
    "IsSuperUserOrReadOnly",
]
