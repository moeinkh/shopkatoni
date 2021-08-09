from django import forms
import django_filters

from .models import *


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='نام', field_name='name', required=False)
    price__gte = django_filters.NumberFilter(label='قیمت از', field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(label='تا', field_name='price', lookup_expr='lte')
    status = django_filters.BooleanFilter(label='موجود', field_name='status', lookup_expr=Product.available)

    color = django_filters.CharFilter(label='رنگ', field_name='orderproduct__variant__color__name', distinct=True)

    brand = django_filters.CharFilter(label='رنگ', field_name='brand__name')

    class Meta:
        model = Product
        fields = ['name', 'brand']


class VariantFilter(django_filters.FilterSet):
    size = django_filters.ChoiceFilter(label='سایز', field_name='size')

    class Meta:
        model = Variants
        fields = ['size', 'color', 'product']

