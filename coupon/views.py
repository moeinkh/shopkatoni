from django.shortcuts import render, redirect
from .models import Coupon
from .forms import CouponApplyForm
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages

# Create your views here.
@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
            messages.success(request, 'تبریک!! کد تخفیف با موفقیت اعمال شد.')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, 'متاسفم!! چنین کد تخفیفی وجود ندارد.')
    return redirect('cart:shopcart')