import datetime

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

from order_app.models import Order
from store_app.models import Service, StoreRating

from django.conf import settings



@staff_member_required
def admin_dashboard(request):
    order_admin_url = reverse("admin:order_app_order_changelist")
    service_admin_url = reverse("admin:store_app_service_changelist")
    review_admin_url = reverse("admin:store_app_storerating_changelist")

    total_orders = Order.objects.filter(store_id=request.user.userprofile.store_user.id).count()
    total_services = Service.objects.filter(store_id=request.user.userprofile.store_user.id).count()
    total_reviews = StoreRating.objects.filter(store_id=request.user.userprofile.store_user.id).count()

    context = {
        'available_apps': admin.site.get_app_list(request),
        'cards': [
            # {"title": "New Signups", "value": new_signups, "icon": "fa fa-user-plus"},
            # {"title": "Total Users", "value": total_users, "icon": "fa fa-users"},
            # {"title": "Active Users", "value": active_users, "icon": "fa fa-users"},
            # {"title": "Deleted Users", "value": deleted_users, "icon": "fa fa-users"},

            # {"title": "New Purchases", "value": new_purchases, "icon": "fa fa-shopping-cart"},
            {"title": "Services", "value": total_services, "icon": "fa fa-barcode", "route": service_admin_url},
            # {"title": "Active Paid Plans", "value": active_paid_plans, "icon": "fa fa-dollar-sign"},
            {"title": "Store Ratings", "value": total_reviews, "icon": "fa fa-user", 'route': review_admin_url},
            {"title": "Total Orders", "value": total_orders, "icon": "fa fa-shopping-cart", "route": order_admin_url},
        ],
    }
    return render(request, 'admin/dashboard.html', context)


class LoginView(LoginView):
    template_name = 'admin/custom_login.html'


def admin_logout(request):
    logout(request)
    return redirect('/admin')


__all__ = ['admin_dashboard', 'LoginView']
