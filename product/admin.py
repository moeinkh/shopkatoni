import admin_thumbnails
from django.contrib import admin

# Register your models here.
from product.models import Category, Product, Size, Images, Comment, Color, Variants, Brand, Discount, IpAddress, Slider


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    list_filter = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


@admin_thumbnails.thumbnail('image')
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'title', 'image_thumbnail']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'brand', 'category', 'making', 'status', 'purchase_price', 'price', 'discount_price', 'image_tag']
    list_filter = ['name', 'category', 'making', 'status']
    readonly_fields = ('image_tag',)
    search_fields = ('name', )
    list_editable = ('status', )
    inlines = [ProductImageInline, ProductVariantsInline]
    prepopulated_fields = {'slug': ('name',)}

    actions = ['dis']

    def dis(self, request, queryset):
        from math import ceil

        for v in queryset:
            if v.discount is not None:
                v.discount_price = True
                dis = v.discount.discount
                v.dis_price = ceil(v.price - dis)
                v.save(update_fields=['dis_price', 'discount_price'])
    dis.short_description = 'اعمال تخفیف'


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['created']
    prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created', 'active']
    list_filter = ['active', 'created']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'id']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'product', 'color', 'size', 'size_id', 'number', 'image_tag']
    list_filter = ['product']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount', 'jvalid_from', 'jvalid_to', 'active']
    filter_horizontal  = ('product', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images, ImageAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(IpAddress)
admin.site.register(Slider)
