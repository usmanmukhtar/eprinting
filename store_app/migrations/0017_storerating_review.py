# Generated by Django 4.2.5 on 2024-01-26 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0016_remove_store_ratings_storerating_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='storerating',
            name='review',
            field=models.TextField(blank=True, null=True),
        ),
    ]
