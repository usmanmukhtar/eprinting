from store_app import views
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()

router.register(r'',views.StoreViewSet, basename='stores')
router.register(r'services', views.ServiceViewSet, basename='services')

urlpatterns = router.urls