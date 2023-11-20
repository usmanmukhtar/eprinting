from django.contrib import admin
from .models import UserProfile
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.forms import ModelForm, PasswordInput
from django import forms
from core_app.mixins import RemoveAdminDefaultMessageMixin


# class GHINUserForm(ModelForm):
#     password = forms.CharField(widget=PasswordInput(), required=False)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['password'].widget.attrs['class'] = 'vTextField'
#         self.fields['password'].widget.attrs['placeholder'] = "Update password"

#     class Meta:
#         model = GHINUser
#         widgets = {
#             'password': PasswordInput(),
#         }
#         fields = ('username', 'password')


# @admin.register(GHINUser)
# class GHINUserAdmin(RemoveAdminDefaultMessageMixin, admin.ModelAdmin):
#     form = GHINUserForm
#     list_display = (
#         "username",
#     )

#     list_display_links = (
#         "username",
#     )

#     def has_add_permission(self, request) -> bool:
#         return False

#     def has_delete_permission(self, request, obj=None) -> bool:
#         return False

#     def save_model(self, request, obj, form, change):
#         self.message_user(request, 'save success!')
#         return super().save_model(request, obj, form, change)

#     def changelist_view(self, request, extra_context=None):
#         if self.model.objects.all().count() == 1:
#             obj = self.model.objects.all()[0]
#             return HttpResponseRedirect(reverse("admin:%s_%s_change" %(self.model._meta.app_label, self.model._meta.model_name), args=(obj.id,)))
#         return super(GHINUserAdmin, self).changelist_view(request=request, extra_context=extra_context)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "image_tag",
        "mobile_number",
        "gender",
    )

    list_display_links = (
        'id',
        'email'
    )

    list_filter = (
        'active',
    )

    search_fields = (
        "full_name",
        "user__email",
    )

    sortable_by = (
        "id",
    )

    date_hierarchy = 'created_at'


    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50"/>'.format(obj.image))
        return '-'

    def email(self, obj):
        return obj.user.email

    def phone_number(self, obj):
        return obj.mobile_number

    image_tag.short_description = 'Image'
    email.short_description = 'Email'
    phone_number.short_description = 'Phone'

    list_per_page = 10

    def has_add_permission(self, request) -> bool:
        return False