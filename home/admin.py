from django.contrib import admin

# Register your models here.
from home.models import Setting, Article, Contact

# Admin Header Change
admin.site.site_header = 'سایت جنگویی شاپ کتونی'


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'phone', 'address']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'created']

admin.site.register(Article)