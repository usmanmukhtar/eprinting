# Generated by Django 4.2.5 on 2024-01-26 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0012_alter_favoritestore_favorited_by_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favoritestore',
            unique_together=set(),
        ),
    ]
