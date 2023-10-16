from rest_framework import permissions

class UserProfileUpdatePermission(permissions.BasePermission):
    """
    Permission class to check that a user can update his own resource only
    """

    def has_permission(self, request, view):
        # check that its an update request and user is modifying his resource only
        if view.action == 'update' and view.kwargs['id']!=request.user.id:
            return False # not grant access
        return True # grant access otherwise