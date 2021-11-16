from django.contrib import admin

# Register your models here.
from order.models import OrderProduct, Order


class OrderProductLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('product', 'variant', 'price', 'quantity', 'total_price')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'postal_code', 'status', 'jcreated']
    list_filter = ['status', 'created', 'paid']
    readonly_fields = ('first_name', 'last_name', 'user', 'postal_code', 'code', 'address', 'city', 'phone', 'paid')
    can_delete = False
    inlines = [OrderProductLine]
    actions = ['send_status', 'cancel_status']
    search_fields = ['code', 'first_name', 'last_name']

    def send_status(self, request, queryset):
        for qw in queryset:
            qw.status = 'ارسال شد'
            qw.save(update_fields=['status'])
    send_status.short_description = 'ارسال شد'

    def cancel_status(self, request, queryset):
        for qw in queryset:
            qw.status = 'کنسل شد'
            qw.save(update_fields=['status'])
    cancel_status.short_description = 'کنسل شد'




admin.site.register(Order, OrderAdmin)