from django.contrib import admin

# Register your models here.
from order.models import ShopCart, OrderProduct, Order


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'price', 'amount']
    list_filter = ['user']
    readonly_fields = ('price', 'amount')


class OrderProductLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price', 'quantity', 'amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'postal_code', 'total', 'status', "jcreated"]
    list_filter = ['status', 'created']
    readonly_fields = ('first_name', 'last_name', 'user', 'postal_code', 'code', 'address', 'city', 'phone', 'total')
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


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'amount']
    list_filter = ['user', 'product']


admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)