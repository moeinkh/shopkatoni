# Generated by Django 3.1.2 on 2021-11-14 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_paid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShopCart',
        ),
    ]
