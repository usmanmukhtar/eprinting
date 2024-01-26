from auth_app.models import UserOtp
from auth_app.serializers import LoginSerializer, LogoutSerializer, RegisterSerializer, \
    ForgetPasswordSerializer, ResetPasswordSerializer, OtpVerificationSerializer, ChangePasswordSerializer, \
    SocialLoginSerializer, RegistrationOtpVerificationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

from core_app.utils import error_response, success_response
# from auth_app.tasks import send_otp_registration


from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserCreationForm, UserProfileForm, StoreForm

def signup_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        user_profile_form = UserProfileForm(request.POST, request.FILES)
        store_form = StoreForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid() and store_form.is_valid():
            user = user_form.save(commit=False)   # Don't save the user instance yet
            user.is_staff = True  # Set is_staff to True
            user.is_superuser = True  # Set is_superuser to True
            user.save()  # Now save the user instance
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()

            # Split the combined address
            combined_address = store_form.cleaned_data.get('address')
            # address_components = [component.strip() for component in combined_address.split(',')]

            store = store_form.save(commit=False)
            store.address = combined_address
            store.user = user_profile
            store.save()

            # Log out any currently logged-in user before redirecting to the login page
            logout(request)

            # Construct the login URL with the 'next' query parameter
            login_url = reverse('admin:login') + '?next=/admin_dashboard/'
            return HttpResponseRedirect(login_url)
    else:
        user_form = UserCreationForm()
        user_profile_form = UserProfileForm()
        store_form = StoreForm()

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'store_form': store_form
    }

    return render(request, 'signup.html', context)



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
