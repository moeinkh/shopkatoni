# Generated by Django 3.1.2 on 2021-11-13 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20211110_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='پرداخت شد؟'),
        ),
    ]
