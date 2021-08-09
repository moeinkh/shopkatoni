from django import template
from django.urls import reverse

from mysite import settings
from order.models import ShopCart
from product.models import Category

register = template.Library()


@register.simple_tag
def shopcart_count(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count