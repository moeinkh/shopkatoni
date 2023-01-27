from celery import shared_task
from .models import Discount, Product
from django.utils import timezone
from mysite.celery import app

@shared_task
def discount_apply():
    discounts = Discount.objects.all()
    products = Product.objects.all()
    for discount in discounts:
        if timezone.now() >= discount.valid_from and timezone.now() <= discount.valid_to:
            discount.active = True
            discount.save()
            for product in discount.product.all():
                product.dis_price = (product.price - discount.discount)
                product.discount_price = True
                product.save()
        else:    
            discount.active = False
            discount.save()
            for product in discount.product.all():
                product.dis_price = None
                product.discount_price = False
                product.save()    


         