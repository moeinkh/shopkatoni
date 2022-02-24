from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .decorators import unauthenticated_user, allowed_users

# Create your views here.
from django.urls import reverse

from django.db.models import Count, Sum, Max
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
    sale = OrderProduct.objects.filter(order__status='ارسال شد').values(
        'product__name',
        ).annotate(
            Sum('quantity'), 
            Max('product__purchase_price'),
            Max('product__price'),
            Sum('total_price'),
            each_income = Max('product__price') - Max('product__purchase_price'),
            income = Sum('quantity') * (Max('product__price') - Max('product__purchase_price'))
            ).order_by('-quantity__sum')    

    user_activity_objects = OnlineUserActivity.get_user_activities()
    number_of_active_users = user_activity_objects.count()

    context = {
        'orders': Order.objects.filter(status='در حال بررسی').order_by('-id'),
        'users_count': User.objects.all().count(),
        'sale': sale,
        'number_of_active_users': number_of_active_users,
        'pro_count': Product.objects.all(),
    }
    return render(request, 'account/admin_panel.html', context)

@allowed_users
def admin_orders(request):
    orders = Order.objects.all()
    search = request.GET.get('search')
    if search:
        orders = Order.objects.filter(
            Q(user__username__icontains=search) |
            Q(code__exact=search))

    return render(request, 'account/admin_orders.html', {
        'orders': orders
    })

@allowed_users
def admin_orders_details(request, id):
    order = get_object_or_404(Order, id=id)

    return render(request, 'account/admin_orders_details.html', {
        'order': order
    })

@allowed_users
def admin_products(request):
    products = Product.objects.all()
    search = request.GET.get('search')
    if search:
        products = Product.objects.filter(
            Q(name__icontains=search) |
            Q(brand__name__icontains=search) 
            )

    return render(request, 'account/admin_products.html', {
        'products': products
    })

@allowed_users
def admin_products_details(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)

    return render(request, 'account/admin_products_details.html', {
        'product': product
    })

@allowed_users
def admin_users(request):
    users = User.objects.all()
    search = request.GET.get('search')
    if search:
        users = User.objects.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(phone_number__icontains=search)
            )

    return render(request, 'account/admin_users.html', {
        'users': users
    })