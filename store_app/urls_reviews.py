from store_app import views
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()

router.register(r'',views.ReviewViewSet, basename='reviews')

urlpatterns = router.urls