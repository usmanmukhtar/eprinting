from auth_app.models import UserOtp
from auth_app.serializers import LoginSerializer, LogoutSerializer, RegisterSerializer, \
    ForgetPasswordSerializer, ResetPasswordSerializer, OtpVerificationSerializer, ChangePasswordSerializer, \
    SocialLoginSerializer, RegistrationOtpVerificationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status

from core_app.utils import error_response, success_response
# from auth_app.tasks import send_otp_registration


class RegisterViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer)
        serializer.save()

        # user = serializer.save()

        # # sending email via celery
        # code = UserOtp.generate_otp(user.id)
        # send_otp_registration.delay(code, user.email)

        return success_response(serializer=serializer, message="User created successfully", status_code=201)


class RegistrationOtpVerificationViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = RegistrationOtpVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer)
        serializer.save()
        return success_response(serializer=serializer, message="OTP Verified Successfully")


class LoginViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer,'Token created successfully')
            # return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return error_response(serializer)


class LogoutViewSet(viewsets.ViewSet):
    serializer_class = LogoutSerializer

    def create(self, request):
        serializer = self.serializer_class(data={'success': True})
        if serializer.is_valid():
            serializer.save(request)
            return success_response(serializer, 'Logged out successfully')
        else:
            return error_response(serializer)


class ForgetPasswordViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = ForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer)
        serializer.save()
        return success_response(serializer=serializer, message="OTP Sent Successfully")


class ResendOtpViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = ForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer)
        serializer.save()
        return success_response(serializer=serializer, message="OTP Sent Successfully")


class OtpVerificationViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = OtpVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer)
        serializer.save()
        return success_response(serializer=serializer, message="OTP Verified Successfully")


class ResetPasswordViewSet(viewsets.ViewSet):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if not serializer.is_valid():
            return error_response(serializer)
        serializer.save(request)
        return success_response(serializer=serializer, message="Password Reset Successful")


class ChangePasswordViewSet(viewsets.ViewSet):
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if not serializer.is_valid():
            return error_response(serializer)
        serializer.save(request)
        return success_response(serializer=serializer, message="Password changed successfully")



class SocialLoginViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SocialLoginSerializer


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer,'Token created successfully')
        else:
            return error_response(serializer)
