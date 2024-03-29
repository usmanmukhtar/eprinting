"""eprintingapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from auth_app.views import signup_view
# from auth_app.admin import custom_admin_site
from django.conf.urls.static import static
from django.conf import settings
from dashboard.views import LoginView, admin_dashboard, admin_logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path(f"{settings.ADMIN_URL}login/", LoginView.as_view(), name='account_login'),
    path(f"{settings.ADMIN_URL}logout/", admin_logout, name='admin_logout'),
    path('signup/', signup_view, name='signup'),
    path(f"admin/login/", auth_views.LoginView.as_view(template_name='admin/custom_login.html'), name='admin_login'),
    path('api/user/', include('user_app.urls')),
    path('api/auth/', include('auth_app.urls')),
    path('api/stores/', include('store_app.urls')),
    path('api/reviews/', include('store_app.urls_reviews')),
    path('api/order/', include('order_app.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)