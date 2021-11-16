from datetime import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator

from coupon.models import Coupon
from user.models import User
from django.db import models
from extensions.utils import jalali_converter

# Create your models here.
from product.models import Product, Variants, Discount


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
    paid = models.BooleanField('پرداخت شد؟', default=False)
    STATUS_CHOICES = (
        ('در حال بررسی', 'در حال بررسی'),
        ('ارسال شد', 'ارسال شد'),
        ('کنسل شد', 'کنسل شد'),
    )
    status = models.CharField('وضعیت', choices=STATUS_CHOICES, max_length=50, default='در حال بررسی')

    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True, verbose_name='کد تخفیف')
    discount = models.IntegerField('تخفیف', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    created = models.DateTimeField('ایجاد', auto_now_add=True)
    updated = models.DateTimeField('به روز رسانی', auto_now=True)

    def __str__(self):
        return self.first_name

    def jcreated(self):
        return jalali_converter(self.created)
    jcreated.short_description = 'تاریخ سفارش'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))

    get_total_cost.short_description = 'مبلغ کل'


class OrderProduct(models.Model):
    class Meta:
        verbose_name = 'سفارش محصول'
        verbose_name_plural = 'سفارش محصول'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='مشخصه')  # relation with variant
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='محصول')
    quantity = models.IntegerField('تعداد')
    price = models.IntegerField('قیمت')
    total_price = models.PositiveIntegerField('قیمت کامل')

    created = models.DateTimeField('ایجاد', auto_now_add=True)
    updated = models.DateTimeField('به روز رسانی', auto_now=True)

    def __str__(self):
        return self.variant.product.name

    def get_cost(self):
        return self.quantity * self.price