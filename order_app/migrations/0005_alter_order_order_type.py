# Generated by Django 4.2.5 on 2024-01-31 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0004_order_order_type_alter_order_orientation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.PositiveIntegerField(choices=[(0, 'Order Placed'), (1, 'Accepted'), (2, 'In Progress'), (3, 'Cancelled'), (4, 'Completed')], default=2),
        ),
    ]
