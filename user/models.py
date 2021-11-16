from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    city = models.CharField('شهر', max_length=75, null=True, blank=True)
    address = models.CharField('آدرس', max_length=250, null=True, blank=True)
    phone_number = models.CharField('تلفن', max_length=11, null=True, blank=True)
    postal_code = models.CharField('کد پستی', max_length=11, null=True, blank=True)

