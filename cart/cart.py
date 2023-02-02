from decimal import Decimal
from django.conf import settings
from product.models import Product, Variants

from coupon.models import Coupon


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        variant_ids = self.cart.keys()
        # get the product objects and add them to the cart
        variants = Variants.objects.filter(id__in=variant_ids)

        cart = self.cart.copy()
        for variant in variants:
            cart[str(variant.id)]['variant'] = variant

        for item in cart.values():
            variant = Variants.objects.get(title=item['variant'])
            if variant.discount_status == True:
                item['price'] = Decimal(variant.discount_price)
                item['total_price'] = item['price'] * item['quantity']
            else:
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, variant, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        variant_id = str(variant.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {'quantity': 0,
                                      'price': str(variant.price)}
        if override_quantity:
            self.cart[variant_id]['quantity'] = quantity
        else:
            self.cart[variant_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, variant):
        """
        Remove a product from the cart.
        """
        variant_id = str(variant.id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()