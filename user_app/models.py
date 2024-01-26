from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


from core_app.models import TimeStampModel, ActiveModel


class UserProfile(TimeStampModel, ActiveModel):
    GENDER_CHOICES = (
        ('N', 'Not specified'),
        ('M','Male'),
        ('F','Female'),
    )

    def user_profile_dir(instance, filename):
        return "backend/user_profile/%s" % (filename)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True)
    mobile_number = models.CharField(max_length=15,null=True, blank=True)
    image = models.ImageField(upload_to=user_profile_dir, max_length=500, null=True, blank=True)
    allow_notifications = models.BooleanField(default=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=500, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')


    @property
    def email(self):
        return self.user.email

    @property
    def is_social_login(self):
        return self.user.is_social_login


    @staticmethod
    def calculate_age(dob):
        try:
            today = timezone.now().date()
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        except:
            return None

    @property
    def age(self):
        return self.calculate_age(self.dob)


    def __str__(self):
        return f'{self.user.first_name if self.user else str("N/A")} {self.user.last_name if self.user else ""}'

    class Meta:
        db_table = "user_profile"

class FavouritePlayers(TimeStampModel):
    favourite_player = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followed_by')
    followed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favourite_player')

    class Meta:
        managed = True
        db_table = 'favourite_players'

        constraints = [
            models.UniqueConstraint(fields=['favourite_player', 'followed_by'], name="user_pair")
        ]

class UserBetPaymentInfo(TimeStampModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bet_payments_info')
    payment_method_name = models.CharField(max_length=50)
    payment_method_url = models.CharField(max_length=256)

    class Meta:
        managed = True
        db_table = 'user_bet_payment_info'
        # TODO: to add this validation or not?
        # constraints = [
        #     models.UniqueConstraint(fields=['user', 'payment_method_name'], name="user_payment_method_name_pair")
        # ]

# TODO: Made a CRUD for admin panel
class ReportType(ActiveModel, TimeStampModel):
    report_type = models.CharField(max_length=2048)

    class Meta:
        db_table = 'report_type'

class ReportUser(TimeStampModel):
    reportee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reported_by')
    reported = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reportee')
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'report_user'