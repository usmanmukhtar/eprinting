# Generated by Django 4.2.5 on 2024-01-26 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_alter_userprofile_image'),
        ('store_app', '0011_alter_favoritestore_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritestore',
            name='favorited_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_favorited_by', to='user_app.userprofile'),
        ),
        migrations.AlterField(
            model_name='favoritestore',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_store', to='store_app.store'),
        ),
    ]
