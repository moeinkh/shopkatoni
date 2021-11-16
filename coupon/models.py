from django.db import models
from extensions.utils import jalali_converter


# Create your models here.
class Coupon(models.Model):
    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'

    code = models.CharField('کد', max_length=128, unique=True)
    discount = models.IntegerField('تخفیف')
    valid_from = models.DateTimeField('از تاریخ')
    valid_to = models.DateTimeField('تا تاریخ')
    active = models.BooleanField('فعال؟')

    def __str__(self):
        return self.code

    def jvalid_from(self):
        return jalali_converter(self.valid_from)
    jvalid_from.short_description = 'از تاریخ'

    def jvalid_to(self):
        return jalali_converter(self.valid_to)
    jvalid_to.short_description = 'تا تاریخ'