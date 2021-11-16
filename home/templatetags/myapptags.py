from django import template
from django.urls import reverse

from mysite import settings
from product.models import Category

register = template.Library()


