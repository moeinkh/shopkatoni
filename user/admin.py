from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

UserAdmin.fieldsets[1][1]['fields'] = (
                ('first_name', 'last_name', 'email', 'city', 'address', 'phone_number', 'postal_code'),
)


admin.site.register(User, UserAdmin)