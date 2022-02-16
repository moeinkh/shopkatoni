from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from product.models import Product, Variants
from .cart import Cart
from .forms import CartAddProductForm
from coupon.forms import CouponApplyForm
from coupon.models import Coupon
from django.contrib import messages

@require_POST
def cart_add(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(Variants, id=variant_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(variant=variant,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:shopcart')


@require_POST
def cart_remove(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(Variants, id=variant_id)
    cart.remove(variant)
    return redirect('cart:shopcart')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    coupon_apply_form = CouponApplyForm()

    return render(request, 'cart/shopcart.html',
                           {
                               'cart': cart,
                            })