from django.contrib import admin
from order_app.models import Order
from django.utils.timezone import localtime

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(store=request.user.userprofile.store_user)

    list_display = (
        "user",
        "service",
        "pickup_time_time"
    )

    list_display_links = (
        'user',
    )

    # list_filter = (
    #     'pickup_time',
    # )

    search_fields = (
        'user',
        'service'
    )

    sortable_by = (
        "id",
    )


    def pickup_time_time(self, obj):
        # Format the time.
        return localtime(obj.pickup_time).strftime('%I:%M %p') if obj.pickup_time else ''

    pickup_time_time.admin_order_field = 'pickup_time'  # Allows column order sorting
    pickup_time_time.short_description = 'Pickup Time'  # Renames column head

