# Generated by Django 3.1.2 on 2023-01-31 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20230121_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='gender',
        ),
        migrations.AddField(
            model_name='variants',
            name='dis_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت با تخفیف'),
        ),
        migrations.AddField(
            model_name='variants',
            name='discount_price',
            field=models.BooleanField(default=False, verbose_name='تخفیف'),
        ),
    ]