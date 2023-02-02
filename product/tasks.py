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
                product.discount_price = (product.price - discount.discount)
                product.discount_status = True
                for variant in product.variants.all():
                    variant.discount_price = (product.price - discount.discount)
                    variant.discount_status = True
                    variant.save()
                product.save()
        else:    
            discount.active = False
            discount.save()
            for product in discount.product.all():
                product.discount_price = None
                product.discount_status = False
                for variant in product.variants.all():
                    variant.discount_price = None
                    variant.discount_status = False
                    variant.save()
                product.save()    


         