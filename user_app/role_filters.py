from django.db.models import Q
from rest_framework_role_filters.role_filters import RoleFilter
from rest_framework.exceptions import PermissionDenied


class SuperAdminRoleFilter(RoleFilter):
    role_id = 'SA'

    def get_queryset(self, request, view, queryset):
        print("INSIDE SUPER ADMIN-----------------------------------")
        return queryset


class RegulerUserRoleFilter(SuperAdminRoleFilter):
    role_id = 'RG'

    def get_allowed_actions(self, request, view, obj=None):
        print("INSIDE REGULAR USER----------------------------------")

        action_role_id = request.data.get('role')

        # Regular user cannot create or update role gte to its role
        if request.method == 'POST':
            if view.action == 'create' and action_role_id == 'SA':
                raise PermissionDenied()
            if view.action == 'update' and action_role_id == 'SA':
                raise PermissionDenied()
            return [view.action]
        # If Action is me then Regular user can GET,PUT,PATCH on his profile
        if request.method in ['GET', 'PUT', 'PATCH']:
            # Regular user cannot update his role itself
            if request.method in ['PUT', 'PATCH'] and "role" in request.data:
                raise PermissionDenied()
            return [view.action]

        raise PermissionDenied()

    def get_queryset(self, request, view, queryset):
        return queryset.filter(role='RG', active=True)
