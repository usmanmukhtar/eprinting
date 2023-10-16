from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    active = models.BooleanField(db_index=True,default=True)

    class Meta:
        abstract = True

