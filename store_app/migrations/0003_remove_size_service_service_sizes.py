# Generated by Django 4.2.5 on 2023-11-11 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0002_service_store_end_time_store_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='size',
            name='service',
        ),
        migrations.AddField(
            model_name='service',
            name='sizes',
            field=models.ManyToManyField(related_name='service_sizes', to='store_app.size'),
        ),
    ]
