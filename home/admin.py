from django.contrib import admin

# Register your models here.
from home.models import Setting, Article

# Admin Header Change
admin.site.site_header = 'سایت جنگویی شاپ کتونی'


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'phone', 'address']


admin.site.register(Article)