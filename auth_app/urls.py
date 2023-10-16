from rest_framework.routers import DefaultRouter
from auth_app import views

router = DefaultRouter()

router.register(r'register', views.RegisterViewSet, basename='register')
router.register(r'verify_registration', views.RegistrationOtpVerificationViewSet, basename='register-otp')


router.register(r'login', views.LoginViewSet, basename='login')
router.register(r'logout', views.LogoutViewSet, basename='logout')
router.register(r'social_login', views.SocialLoginViewSet, basename='social-login')

router.register(r'forget_password', views.ForgetPasswordViewSet, basename='forget-password')
router.register(r'otp/resend', views.ResendOtpViewSet, basename="resend-otp")
router.register(r'otp/verify', views.OtpVerificationViewSet, basename="verify-otp")
router.register(r'reset_password', views.ResetPasswordViewSet, basename='reset-password')
router.register(r'change_password', views.ChangePasswordViewSet, basename='change-password')


urlpatterns = router.urls
