# Generated by Django 3.1.2 on 2021-11-09 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=5, verbose_name='کد خرید')),
                ('first_name', models.CharField(max_length=150, verbose_name='نام')),
                ('last_name', models.CharField(max_length=150, verbose_name='نام خانوادگی')),
                ('phone', models.CharField(blank=True, max_length=11, verbose_name='تلفن')),
                ('address', models.CharField(max_length=250, verbose_name='آدرس')),
                ('city', models.CharField(max_length=75, verbose_name='شهر')),
                ('postal_code', models.CharField(max_length=11, verbose_name='کد پستی')),
                ('total', models.IntegerField(verbose_name='کل')),
                ('status', models.CharField(choices=[('در حال بررسی', 'در حال بررسی'), ('ارسال شد', 'ارسال شد'), ('کنسل شد', 'کنسل شد')], default='در حال بررسی', max_length=50, verbose_name='وضعیت')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='به روز رسانی')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارش',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='تعداد')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('amount', models.IntegerField(verbose_name='قیمت کل')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='به روز رسانی')),
            ],
            options={
                'verbose_name': 'سفارش محصول',
                'verbose_name_plural': 'سفارش محصول',
            },
        ),
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='تعداد')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': 'سبد خرید',
            },
        ),
    ]
