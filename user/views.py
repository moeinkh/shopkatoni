from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash


from .decorators import unauthenticated_user, allowed_users

# Create your views here.
from django.urls import reverse

from django.db.models import Count, Sum
from order.models import Order, OrderProduct, ShopCart
from product.models import Category, Product
from user.forms import SignupForm, UserEditForm
from .models import User


from online_users.models import OnlineUserActivity
from datetime import timedelta


@login_required(login_url='registration:login')
def user_profile(request):
    profile = User.objects.get(pk=request.user.pk)
    context = {
        'profile': profile,
    }
    return render(request, 'registration/profile.html', context)


@login_required(login_url='registration:login')
def user_editprofile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'پروفایل با موفقیت تغییر کرد')
            return HttpResponseRedirect(reverse('registration:profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        context = {
            'user_form': user_form,
        }
        return render(request, 'registration/editprofile.html', context)


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'نام کاربری یا رمز عبور نادرست می باشد')
            return HttpResponseRedirect(reverse('registration:login'))
    context = {

    }
    return render(request, 'registration/login.html', context)


@login_required(login_url='registration:login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('registration:login'))


@unauthenticated_user
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('home:home'))
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse('registration:signup'))
    form = SignupForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'registration/registration.html', context)


@login_required(login_url='registration:login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
            return HttpResponseRedirect(reverse('registration:profile'))
        else:
            messages.error(request, ':لطفا خطا را رفع نمایید</br> ' + str(form.errors))
            return HttpResponseRedirect(reverse('registration:password_change'))
    else:
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
        }
        return render(request, 'registration/password_change.html', context)


@login_required(login_url='registration:login')
def user_orders(request):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.filter(user_id=current_user.id).order_by('-created')
    context = {
        'category': category,
        'order': order,
    }
    return render(request, 'registration/user_orders.html', context)


@login_required(login_url='registration:login')
def user_orderdetails(request, id):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'registration/user_order_details.html', context)


@allowed_users
def adminpnl(request):
    sale = OrderProduct.objects.values('order__status', 'product__name').annotate(Sum('quantity'), Sum('amount')).order_by('-quantity__sum')

    user_activity_objects = OnlineUserActivity.get_user_activities()
    number_of_active_users = user_activity_objects.count()

    context = {
        'orders': Order.objects.filter(status='در حال بررسی').order_by('-id'),
        'users_count': User.objects.all().count(),
        'sale': sale,
        'number_of_active_users': number_of_active_users,
        'pro_count': Product.objects.all()
    }
    return render(request, 'registration/admin_panel.html', context)

