from django import forms
from .models import ShopCart, Order
from user.models import User


class ShopCartForm(forms.ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class OrderForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'postal_code', 'address', 'city']
