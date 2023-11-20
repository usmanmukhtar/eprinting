from django.contrib import admin
from .models import Store, Service, Size

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "store",
    )

    list_display_links = (
        'name',
    )

    list_filter = (
        'price',
    )

    search_fields = (
        "name",
    )

    sortable_by = (
        "id",
    )

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price"
    )

    list_display_links = (
        'name',
    )

    list_filter = (
        'price',
    )

    search_fields = (
        "name",
    )

    sortable_by = (
        "id",
    )