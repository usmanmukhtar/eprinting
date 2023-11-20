from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# from rest_framework.exceptions import APIException

from auth_app.manager import UserManager
from user_app.models import UserProfile

import random


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    username = None
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_or_none(**kwargs):
        try:
            return User.objects.get(**kwargs)
        except User.DoesNotExist:
            return None

    def create_user_profile(self, **kwargs):
        return UserProfile.objects.create(user=self, **kwargs)

    @staticmethod
    def send_welcome_note(email, full_name, *args, **kwargs) -> bool:
        context = {'email': email, 'full_name': full_name}

        email_html_message = render_to_string('email/welcome.html', context)
        email_plaintext_message = ''

        try:
            msg = EmailMultiAlternatives(
                "WELCOME", email_plaintext_message, settings.EMAIL_HOST_USER, [email]
            )
            msg.attach_alternative(email_html_message, "text/html")
            msg.send()
            # TODO : Replace Exception with SMTPException
        except Exception as e:
            return False
        else:
            return True

    @staticmethod
    def send_account_deletion_note(email, full_name, *args, **kwargs):
        context = {'email': email, 'full_name': full_name}

        email_html_message = render_to_string('email/account_delete.html', context)
        email_plaintext_message = ''

        try:
            msg = EmailMultiAlternatives(
                "ACCOUNT SUCCESSFULLY REMOVED", email_plaintext_message, settings.EMAIL_HOST_USER, [email]
            )
            msg.attach_alternative(email_html_message, "text/html")
            msg.send()
            # TODO : Replace Exception with SMTPException
        except Exception as e:
            return False
        else:
            return True


    class Meta:
        managed = True
        db_table = 'user'


class UserOtp(models.Model):
    code = models.CharField(max_length=6, verbose_name="OTP Code")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)


    class Meta:
        unique_together = ("user", "code")

    def is_expired(self, time_limit=None):
        current_datetime = timezone.now()
        return current_datetime <= time_limit if time_limit else not current_datetime <= self.updated_at + settings.OTP_EXPIRE_DURATION

    @staticmethod
    def verify_otp(code, user__id, time_limit=None):
        user_otp_object = UserOtp.objects.filter(code=code, user__id=user__id).first()
        return not user_otp_object.is_expired(time_limit) if user_otp_object else False

    @staticmethod
    def _generate_otp(user__id: int):
        try:
            user_otp_obj = UserOtp.objects.get(user__id=user__id)
        except UserOtp.DoesNotExist as e:
            return None
        else:
            return user_otp_obj.delete()

    @staticmethod
    def generate_otp(user__id):
        code_ranges = {
            4: f"{random.randint(0000, 9999):04}",
            5: f"{random.randint(00000, 99999):05}",
            6: f"{random.randint(000000, 999999):06}",
        }
        code_length = settings.OTP_CODE_LENGTH

        code = code_ranges[code_length]
        UserOtp._generate_otp(user__id)
        UserOtp.objects.create(code=code, user=User.objects.get(id=user__id))
        return code

    @staticmethod
    def send_otp(email, code, *args, **kwargs) -> bool:
        context = {'email': email, 'otp': code}
        email_html_message = render_to_string('email/otp.html', context)
        # email_plaintext_message = render_to_string('email/otp.txt', context)
        email_plaintext_message = ''

        try:
            msg = EmailMultiAlternatives(
                "OTP VERIFICATION", email_plaintext_message, settings.EMAIL_HOST_USER, [email]
            )
            msg.attach_alternative(email_html_message, "text/html")
            msg.send()
            print("email sent inside try")
            # TODO : Replace Exception with SMTPException
        except Exception as e:
            print("except : ",e)
            return False
        else:
            print("else")
            return True