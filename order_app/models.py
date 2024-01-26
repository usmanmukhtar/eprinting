from django.db import models
from core_app.models import TimeStampModel
from user_app.models import UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator
from store_app.models import Store, Service, Size

# Create your models here.

class OrientationType(models.IntegerChoices):
    portrait = 1, "Portrait"
    landscape = 2, "Landscape"

class Order(TimeStampModel):

    def order_dir(instance, filename):
        return "backend/orders/%s-%s" % (instance.id, filename)

    ORIENTATION_TYPE = OrientationType
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='order_store')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='order_service')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='order_size')
    doc_type = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    orientation = models.PositiveIntegerField(choices=ORIENTATION_TYPE.choices, default=OrientationType.portrait)
    notes = models.TextField(blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    document = models.FileField(upload_to=order_dir)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_user')

    class Meta:
        db_table = 'order'

    def __str__(self):
        return f'{self.service.name or str("N/A")}'