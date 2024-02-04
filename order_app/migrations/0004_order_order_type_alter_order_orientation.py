# Generated by Django 4.2.5 on 2024-01-31 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0003_alter_order_orientation'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_type',
            field=models.PositiveIntegerField(choices=[(0, 'In Progress'), (1, 'Cancelled'), (2, 'Completed')], default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='orientation',
            field=models.PositiveIntegerField(choices=[(1, 'Portrait'), (2, 'Landscape')], default=1),
        ),
    ]