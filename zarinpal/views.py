from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
# Github.com/Rasooll
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client

MERCHANT = '6705e547-3113-4357-9e3e-0107e3e08142'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/zarinpal/verify/' # Important: need to edit for realy server.


def send_request(request):
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')


# from django.shortcuts import render, get_object_or_404

# # Create your views here.
# # -*- coding: utf-8 -*-
# # Github.com/Rasooll
# from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse
# from django.shortcuts import redirect
# from zeep import Client
# from order.models import Order



# MERCHANT = '6705e547-3113-4357-9e3e-0107e3e08142'
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# # amount = 1000  # Toman / Required
# CallbackURL = 'http://shopkatoni.ir/payment/verify/' # Important: need to edit for realy server.


# def send_request(request):
#     order_id = request.session.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
#     total_cost = order.get_total_cost()
#     amount = total_cost
#     result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
#     if result.Status == 100:
#         return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
#     else:
#         return HttpResponse('Error code: ' + str(result.Status))


# def verify(request):
#     if request.GET.get('Status') == 'OK':
#         result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
#         if result.Status == 100:
#             order_id = request.session.get('order_id')
#             order = get_object_or_404(Order, id=order_id)
#             order.paid = True
#             order.save()
#             return HttpResponseRedirect(reverse('order:ordercomplate'))
#         elif result.Status == 101:
#             return HttpResponse('Transaction submitted : ' + str(result.Status))
#         else:
#             return HttpResponse('تراکنش با شکست مواجه شد.\nStatus: ' + str(result.Status))
#     else:
#         return HttpResponseRedirect(reverse('order:ordercancled'))