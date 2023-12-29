import datetime

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

from order_app.models import Order
from store_app.models import Service
from django.conf import settings



@staff_member_required
def admin_dashboard(request):
    order_admin_url = reverse("admin:order_app_order_changelist")
    total_orders = Order.objects.filter(store_id=request.user.userprofile.store_user.id).count()
    # new_signups = UserProfile.objects.filter(date_joined__date=datetime.date.today()).count()
    # new_purchases = PaymentHistory.objects.filter(created_at__date=datetime.date.today()).count()
    # new_scans = FacialReport.objects.filter(created_at__date=datetime.date.today()).count() + BodyReport.objects.filter(created_at__date=datetime.date.today()).count()
    # total_users = UserProfile.global_objects.count()
    # active_users = UserProfile.objects.count()
    # deleted_users = UserProfile.deleted_objects.count()
    # active_paid_plans = UserScanSubscription.objects.filter(status=UserScanSubscription.STATUS_CHOICES.active, package__type=1).count()
    # active_free_plans = UserScanSubscription.objects.filter(status=UserScanSubscription.STATUS_CHOICES.active, package__type=0).count()

    context = {
        'available_apps': admin.site.get_app_list(request),
        'cards': [
            # {"title": "New Signups", "value": new_signups, "icon": "fa fa-user-plus"},
            # {"title": "Total Users", "value": total_users, "icon": "fa fa-users"},
            # {"title": "Active Users", "value": active_users, "icon": "fa fa-users"},
            # {"title": "Deleted Users", "value": deleted_users, "icon": "fa fa-users"},

            # {"title": "New Purchases", "value": new_purchases, "icon": "fa fa-shopping-cart"},
            # {"title": "New Scans", "value": new_scans, "icon": "fa fa-barcode"},
            # {"title": "Active Paid Plans", "value": active_paid_plans, "icon": "fa fa-dollar-sign"},
            # {"title": "Active Free Plans", "value": active_free_plans, "icon": "fa fa-user"},
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
