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
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='store_user')

    class Meta:
        db_table = 'store'

    def __str__(self):
        return f'{self.name or str("N/A")}'


class Service(models.Model):

    def service_dir(instance, filename):
        return "backend/services/%s-%s" % (instance.id, filename)

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=service_dir, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, related_name='store_services', on_delete=models.CASCADE)
    sizes = models.ManyToManyField('Size', related_name='service_sizes')

    class Meta:
        db_table = 'service'

    def __str__(self):
        return f'{self.name or str("N/A")}'

class Size(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # service = models.ForeignKey(Service, related_name='service_size', on_delete=models.CASCADE)

    class Meta:
        db_table = 'size'

    def __str__(self):
        return f'{self.name or str("N/A")}'

class FavoriteStore(TimeStampModel):
    favorited_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorite_favorited_by')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='favorite_store')

    class Meta:
        db_table = 'favorite_store'

class StoreRating(TimeStampModel):
    liked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='store_rating_liked_by')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_rating_store')
    rate = models.DecimalField(max_digits=3, decimal_places=2, validators = [MinValueValidator(0.0), MaxValueValidator(5.0)])
    review = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'store_rating'