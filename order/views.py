from smtplib import SMTPAuthenticationError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

# Create your views here.
from django.urls import reverse
from django.utils.crypto import get_random_string

from order.forms import ShopCartForm, OrderForm
from order.models import ShopCart, Order, OrderProduct
from product.models import Category, Product, Variants, Discount
from user.models import User


@login_required(login_url='registration:login')
def addtoshop(request, id):
    url = request.META.get('HTTP_REFERER')   # get last url
    current_user = request.user
    product = Product.objects.get(pk=id)

    if product.variant is not None:
        variantid = request.POST.get('variantid')
        checkvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)
        if checkvariant:
            control = 1
        else:
            control = 0
    else:
        checkproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id)   # Check Product in ShopCart
        if checkproduct == 1:
            control = 1   # The Product is in ShopCart
        else:
            control = 0   # The Product is not in ShopCart
    try:
        if request.method == 'POST':
            form = ShopCartForm(request.POST)
            if form.is_valid():
                if control == 1:
                    if product.variant == 'None':
                        data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                    else:
                        data = ShopCart.objects.get(variantid=variantid, user_id=current_user.id)
                    data.quantity += form.cleaned_data['quantity']
                    data.save()
                else:
                    data = ShopCart()
                    data.user_id = current_user.id
                    data.product_id = id
                    data.variant_id = variantid
                    data.quantity = form.cleaned_data['quantity']
                    data.save()
            messages.success(request, 'محصول به سبد خرید اضافه شد')
            return HttpResponseRedirect(reverse('order:shopcart'))

        else:
            if control == 1:
                data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                data.quantity += 1
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = 1
                data.variant_id = None
                data.save()
            messages.success(request, 'محصول به سبد خرید اضافه شد')
            return HttpResponseRedirect(reverse('order:shopcart'))
    except Exception:
        messages.warning(request, 'این محصول قبلا به سبد خرید اضافه شده است، '
                                  'برای افزایش تعداد ابتدا محصول را حذف کرده و سپس سفارش دهید:)')
        return HttpResponseRedirect(reverse('order:shopcart'))


@login_required(login_url='registration:login')
def shopcart(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    post = 40000
    total = 0
    for rs in shopcart:
        if rs.product.dis_price:
            total += rs.product.dis_price * rs.quantity
        else:
            total += rs.product.price * rs.quantity
    context = {
        'category': Category.objects.all(),
        'shopcart': shopcart,
        'total': total,
        'discount': Discount.objects.all(),
        'post': post,
        'total_post': total + post
    }
    return render(request, 'order/shopcart.html', context)


@login_required(login_url='registration:login')
def deletefromshop(request, id):
    shopcart = ShopCart.objects.filter(product_id=id).delete()
    messages.success(request, 'محصول از سبد خرید حذف شد')
    return HttpResponseRedirect(reverse('order:shopcart'))


@login_required(login_url='registration:login')
def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=request.user.id)
    profile = User.objects.get(pk=request.user.pk)

    post = 40000
    total = 0
    for rs in shopcart:
        if rs.product.dis_price:
            total += rs.product.dis_price * rs.quantity
        else:
            total += rs.product.price * rs.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.city = form.cleaned_data['city']
            data.address = form.cleaned_data['address']
            data.phone = form.cleaned_data['phone_number']
            data.postal_code = form.cleaned_data['postal_code']
            data.user_id = current_user.id
            data.total = total
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            shopcart = ShopCart.objects.filter(user_id=request.user.id)
            for item in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = item.product_id
                detail.user_id = current_user.id
                detail.quantity = item.quantity
                detail.price = item.product.price
                detail.variant_id = item.variant_id
                detail.amount = item.amount
                detail.save()

                # کم کردن تعداد محصول
                variant = Variants.objects.get(id=item.variant_id)
                variant.number -= item.quantity
                variant.save()

            ShopCart.objects.filter(user_id=request.user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, 'خرید شما کامل شده. ممنون از اعتماد شما')
            context = {
                'category': category,
                'ordercode': ordercode,
                'shopcart': shopcart,
                'current_user': current_user,
                'total': total,
            }
            try:
                # تنظیمات ارسال فاکتور خرید با ایمیل
                message = get_template('order/mail_order.html').render(context)
                msg = EmailMessage(
                    'فاکتور خرید',
                    message,
                    'shopkatoni99@gmail.com',
                    [request.user.email],
                )
                msg.content_subtype = 'html'
                msg.send()
                print('mail send')
                return render(request, 'order/ordercomplate.html', context)
            except SMTPAuthenticationError:
                messages.error(request, 'متاسفانه مشکلی در سیستم وجود دارد و ایمیل برای شما ارسال نشده است اما خرید شما تکمیل گردید و نگرانی از این بابت نداشته باشید.')
                return render(request, 'order/ordercomplate.html', context)
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse('order:orderproduct'))

    form = OrderForm()
    context = {
        'category': category,
        'shopcart': shopcart,
        'total': total,
        'profile': profile,
        'total_post': total + post
    }
    return render(request, 'order/orderproduct.html', context)





