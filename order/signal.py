from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderProduct, Order


@receiver(post_save, sender=Order)
def create_order_product(sender, instance, created, **kwargs):
    if created:
        OrderProduct.objects.create(order=instance)


@receiver(post_save, sender=Order)
def save_order_product(sender, instance, **kwargs):
    instance.orderproduct.save()