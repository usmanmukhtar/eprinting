from django.db import models
from core_app.models import TimeStampModel
from user_app.models import UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator

class Store(TimeStampModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = 'store'

class OrientationType(models.IntegerChoices):
    portrait = 1, "Portrait"
    landscape = 2, "Landscape"


class Service(models.Model):
    ORIENTATION_TYPE = OrientationType
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, related_name='store_services', on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=255)
    orientation = models.PositiveIntegerField(choices=ORIENTATION_TYPE.choices, default=OrientationType.portrait)

class Size(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service = models.ForeignKey(Service, related_name='service_size', on_delete=models.CASCADE)


class FavoriteStore(TimeStampModel):
    favorited_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        db_table = 'favorite_store'

class StoreRating(TimeStampModel):
    liked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=3, decimal_places=2, validators = [MinValueValidator(0.0), MaxValueValidator(5.0)])

    class Meta:
        db_table = 'store_rating'