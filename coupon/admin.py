from django.contrib import admin
from .models import Coupon

# Register your models here.


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'jvalid_from', 'jvalid_to', 'active']
    list_filter = ['discount', 'active']
    search_fields = ['code']