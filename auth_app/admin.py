from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from store_app.models import Store

# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ['email', 'is_staff', 'is_active']
#     list_filter = ['email', 'is_staff', 'is_active']
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ['email']
#     ordering = ['email']

# admin.site.register(User, CustomUserAdmin)


# class CustomAdminSite(admin.AdminSite):
#     site_header = 'Store Admin'
#     site_title = 'Store Admin Portal'
#     index_title = 'Welcome to Store Admin Portal'

#     def has_permission(self, request):
#         """
#         Override this method to restrict access to only store users or
#         based on some other criteria.
#         """
#         return request.user.is_active and request.user.is_staff

#     def get_app_list(self, request):
#         """
#         Override this method to customize the models that show up in the
#         admin site for store users.
#         """
#         app_list = super().get_app_list(request)
#         if request.user.is_superuser:
#             return app_list

#         # Example: Only show the 'Store' model for store users
#         return [app for app in app_list if app['name'] == 'Store']

# custom_admin_site = CustomAdminSite(name='custom_admin')

# @admin.register(Store, site=custom_admin_site)
# class StoreAdmin(admin.ModelAdmin):
#     pass

from django.contrib.auth.models import Group

admin.site.unregister(Group)