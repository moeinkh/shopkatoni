from datetime import datetime

from user.models import User
from django.db import models
from extensions.utils import jalali_converter

# Create your models here.
from product.models import Product, Variants, Discount


class ShopCart(models.Model):
    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید'

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='مشخصات')
    discounts = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='تخفیف')
    quantity = models.IntegerField('تعداد')

    def __str__(self):
        return self.product.name

    @property
    def price(self):
        return self.product.price

    @property
    def amount(self):
        if self.product.discount:
            return (self.quantity * self.product.dis_price)
        else:
            return (self.quantity * self.product.price)


class Order(models.Model):
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    code = models.CharField('کد خرید', max_length=5, editable=False)
    first_name = models.CharField('نام', max_length=150)
    last_name = models.CharField('نام خانوادگی', max_length=150)
    phone = models.CharField('تلفن', blank=True, max_length=11)
    address = models.CharField('آدرس', max_length=250)
    city = models.CharField('شهر', max_length=75)
    postal_code = models.CharField('کد پستی', max_length=11)
    total = models.IntegerField('کل')
    STATUS_CHOICES = (
        ('در حال بررسی', 'در حال بررسی'),
        ('ارسال شد', 'ارسال شد'),
        ('کنسل شد', 'کنسل شد'),
    )
    status = models.CharField('وضعیت', choices=STATUS_CHOICES, max_length=50, default='در حال بررسی')
    created = models.DateTimeField('ایجاد', auto_now_add=True)
    updated = models.DateTimeField('به روز رسانی', auto_now=True)

    def __str__(self):
        return self.first_name

    def jcreated(self):
        return jalali_converter(self.created)
    jcreated.short_description = 'تاریخ سفارش'


class OrderProduct(models.Model):
    class Meta:
        verbose_name = 'سفارش محصول'
        verbose_name_plural = 'سفارش محصول'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True, null=True)  # relation with varinat
    discounts = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='تخفیف')
    quantity = models.IntegerField('تعداد')
    price = models.IntegerField('قیمت')
    amount = models.IntegerField('قیمت کل')

    created = models.DateTimeField('ایجاد', auto_now_add=True)
    updated = models.DateTimeField('به روز رسانی', auto_now=True)

    def __str__(self):
        return self.product.name

