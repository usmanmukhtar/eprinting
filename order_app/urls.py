from order_app import views
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()

router.register(r'',views.OrderViewSet, basename='orders')

urlpatterns = router.urls