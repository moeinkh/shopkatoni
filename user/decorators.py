from django.shortcuts import redirect
from django.http import HttpResponse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home:home')
    return wrapper_func