from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


from .decorators import unauthenticated_user, allowed_users

# Create your views here.
from django.urls import reverse

from django.db.models import Count, Sum
from order.models import Order, OrderProduct
from product.models import Category, Product
from user.forms import UserEditForm
from .models import User


from online_users.models import OnlineUserActivity
from datetime import timedelta


@login_required(login_url='account:account_login')
def user_profile(request):
    profile = User.objects.get(pk=request.user.pk)
    context = {
        'profile': profile,
    }
    return render(request, 'account/profile.html', context)


@login_required(login_url='account:account_login')
def user_editprofile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'پروفایل با موفقیت تغییر کرد')
            return HttpResponseRedirect(reverse('account:profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        context = {
            'user_form': user_form,
        }
        return render(request, 'account/editprofile.html', context)

@login_required(login_url='account:account_login')
def user_orders(request):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.filter(user_id=current_user.id).order_by('-created')
    context = {
        'category': category,
        'order': order,
    }
    return render(request, 'account/user_orders.html', context)


@login_required(login_url='account:account_login')
def user_orderdetails(request, id):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'account/user_order_details.html', context)


@allowed_users
def adminpnl(request):
    sale = OrderProduct.objects.values('order__status', 'product__name').annotate(Sum('quantity'), Sum('total_price')).order_by('-quantity__sum')

    user_activity_objects = OnlineUserActivity.get_user_activities()
    number_of_active_users = user_activity_objects.count()

    context = {
        'orders': Order.objects.filter(status='در حال بررسی').order_by('-id'),
        'users_count': User.objects.all().count(),
        'sale': sale,
        'number_of_active_users': number_of_active_users,
        'pro_count': Product.objects.all()
    }
    return render(request, 'account/admin_panel.html', context)

