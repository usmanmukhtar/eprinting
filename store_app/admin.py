from django.contrib import admin
from .models import Store, Service, Size, StoreRating

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(store=request.user.userprofile.store_user)
    
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


@admin.register(StoreRating)
class StoreRatingAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(store=request.user.userprofile.store_user)
    
    list_display = (
        "liked_by",
        "rate",
        "review"
    )

    # list_display_links = (
    #     'liked_by',
    # )

    search_fields = (
        "liked_by",
    )

    sortable_by = (
        "id",
    )

    readonly_fields=(
        "liked_by",
        "rate",
        "review",
        "store"
    )
    def has_add_permission(self, request) -> bool:
        return False
    
    def has_delete_permission(self, request, obj=None) -> bool:
        return False
    
    def has_change_permission(self, request, obj=None) -> bool:
        return False

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