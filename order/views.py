from smtplib import SMTPAuthenticationError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage, send_mail

# Create your views here.
from django.urls import reverse
from django.utils.crypto import get_random_string

from cart.cart import Cart
from order.forms import OrderForm
from order.models import OrderProduct
from product.models import Category, Product, Variants


# @login_required(login_url='account:account_login')
# def orderproduct(request):
#     category = Category.objects.all()
#     current_user = request.user
#     shopcart = ShopCart.objects.filter(user_id=request.user.id)
#     profile = User.objects.get(pk=request.user.pk)
#
#     post = 40000
#     total = 0
#     for rs in shopcart:
#         if rs.product.dis_price:
#             total += rs.product.dis_price * rs.quantity
#         else:
#             total += rs.product.price * rs.quantity
#
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             data = Order()
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.city = form.cleaned_data['city']
#             data.address = form.cleaned_data['address']
#             data.phone = form.cleaned_data['phone_number']
#             data.postal_code = form.cleaned_data['postal_code']
#             data.user_id = current_user.id
#             data.total = total
#             ordercode = get_random_string(5).upper()
#             data.code = ordercode
#             data.save()
#
#             shopcart = ShopCart.objects.filter(user_id=request.user.id)
#             for item in shopcart:
#                 detail = OrderProduct()
#                 detail.order_id = data.id
#                 detail.product_id = item.product_id
#                 detail.user_id = current_user.id
#                 detail.quantity = item.quantity
#                 if item.product.dis_price:
#                     detail.price = item.product.dis_price
#                 else:
#                     detail.price = item.product.price
#                 detail.variant_id = item.variant_id
#                 detail.amount = item.amount
#                 detail.save()
#
#                 # کم کردن تعداد محصول
#                 variant = Variants.objects.get(id=item.variant_id)
#                 variant.number -= item.quantity
#                 variant.save()
#
#             ShopCart.objects.filter(user_id=request.user.id).delete()
#             request.session['cart_items'] = 0
#             messages.success(request, 'خرید شما کامل شده. ممنون از اعتماد شما')
#             context = {
#                 'category': category,
#                 'ordercode': ordercode,
#                 'shopcart': shopcart,
#                 'current_user': current_user,
#                 'total': total,
#             }
#             try:
#                 # تنظیمات ارسال فاکتور خرید با ایمیل
#                 message = get_template('order/mail_order.html').render(context)
#                 msg = EmailMessage(
#                     'فاکتور خرید',
#                     message,
#                     'shopkatoni99@gmail.com',
#                     [request.user.email],
#                 )
#                 msg.content_subtype = 'html'
#                 msg.send()
#                 print('mail send')
#                 return render(request, 'order/ordercomplate.html', context)
#             except SMTPAuthenticationError:
#                 messages.error(request, 'متاسفانه مشکلی در سیستم وجود دارد و ایمیل برای شما ارسال نشده است اما خرید شما تکمیل گردید و نگرانی از این بابت نداشته باشید.')
#                 return render(request, 'order/ordercomplate.html', context)
#         else:
#             messages.error(request, form.errors)
#             return HttpResponseRedirect(reverse('order:orderproduct'))
#
#     form = OrderForm()
#     context = {
#         'category': category,
#         'shopcart': shopcart,
#         'total': total,
#         'profile': profile,
#         'total_post': total + post
#     }
#     return render(request, 'order/orderproduct.html', context)


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.user = request.user
            code = get_random_string(8)
            order.code = code
            order.save()
            for item in cart:
                variant = item['variant']
                OrderProduct.objects.create(
                    order=order,
                    product=variant.product,
                    variant=item['variant'],
                    price=item['price'],
                    quantity=item['quantity'],
                    total_price=item['total_price']
                )
                variant = Variants.objects.get(title=item['variant'])
                variant.number -= item['quantity']
                variant.save()
            # clear the cart
            cart.clear()
            # clear the coupon code
            request.session['coupon_id'] = None
            # set order in session
            request.session['order_id'] = order.id
            try:
                # تنظیمات ارسال فاکتور خرید با ایمیل
                subject = 'ثبت سفارش'
                message = f'با سلام و خسته نباشید {request.user.username}'
                send_mail(subject, message, 'coolgertn@gmail.com', [request.user.email], fail_silently=False)
                messages.success(request, 'خرید با موفقیت ثبت شد.')
                return redirect(reverse('home:home'))
            except SMTPAuthenticationError:
                messages.success(request, 'خرید با موفقیت ثبت شد.')
                return redirect(reverse('home:home'))

    else:
        form = OrderForm()
    return render(request, 'order/orderproduct.html', {
        'form': form,
        'cart': cart
    })


