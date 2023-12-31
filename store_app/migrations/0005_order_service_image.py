# Generated by Django 4.2.5 on 2023-11-11 18:59

from django.db import migrations, models
import store_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0004_alter_service_table_alter_size_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=store_app.models.Service.service_dir),
        ),
    ]
