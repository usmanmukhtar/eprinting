# Generated by Django 4.2.5 on 2024-01-26 12:23

from django.db import migrations, models
import order_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='document',
            field=models.FileField(default='', upload_to=order_app.models.Order.order_dir),
            preserve_default=False,
        ),
    ]
