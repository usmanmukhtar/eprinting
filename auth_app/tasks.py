from celery import shared_task
from auth_app.models import UserOtp, User


@shared_task
def send_otp_registration(code, user_email):
    UserOtp.send_otp(user_email, code)
    return {'user_email':user_email,'success':True}


@shared_task
def send_welcome_email(full_name, user_email):
    User.send_welcome_note(user_email, full_name)
    return {'user_email':user_email,'success':True}


@shared_task
def send_account_deletion_email(full_name, user_email):
    User.send_account_deletion_note(user_email, full_name)
    return {'user_email':user_email,'success':True}