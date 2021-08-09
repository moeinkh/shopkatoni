
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import TextInput, EmailInput, Select

from .models import User


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=50, label='نام کاربری :')
    email = forms.EmailField(label='ایمیل :')
    first_name = forms.CharField(max_length=50, help_text='نام', label='نام :')
    last_name = forms.CharField(max_length=50, help_text='نام خانوادگی', label='نام خانوادگی :')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'city', 'address', 'phone_number', 'postal_code')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'username'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last_name'}),
        }

