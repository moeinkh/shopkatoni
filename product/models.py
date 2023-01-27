from extensions.utils import jalali_converter
from user.models import User
from django.db import models
from django.urls import reverse

from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.utils.translation import gettext as _
from django.utils import timezone

# Create your models here.
from django.utils.html import format_html


class Category(models.Model):
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی'

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, verbose_name='زیردسته')
    title = models.CharField('عنوان', max_length=50)
    slug = models.SlugField('اسلاگ', max_length=50, allow_unicode=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:katoni_category', args=[self.slug])


class Brand(models.Model):
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند'
    name = models.CharField('اسم', max_length=50)
    slug = models.SlugField('اسلاگ', max_length=50, allow_unicode=True)
    image = models.ImageField('عکس', upload_to='katoni_images/', null=True, blank=True)
    created = models.DateTimeField('ایجاد', auto_now_add=True)
    updated = models.DateTimeField('به روز رسانی', auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:katoni_brand', args=[self.slug])


class IpAddress(models.Model):
    class Meta:
        verbose_name = 'IP ها'
        verbose_name_plural = 'IP'
    ip_address = models.GenericIPAddressField('آدرس آی پی')

    def __str__(self):
        return self.ip_address


class Product(models.Model):
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصول'

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته بندی')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, max_length=50, verbose_name='برند')
    # discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='تخفیف')
    dis_price = models.PositiveIntegerField('قیمت با تخفیف', blank=True, null=True)
    name = models.CharField('اسم', max_length=50)
    slug = models.SlugField('اسلاگ', max_length=500, allow_unicode=True)
    description = models.TextField('توضیحات')
    price = models.IntegerField('قیمت', default=0)
    purchase_price = models.IntegerField('قیمت خرید', default=0)
    discount_price = models.BooleanField('تخفیف', default=False)

    image = models.ImageField('عکس', upload_to='katoni_images/', null=True, blank=True)

    available = 1
    unavailable = 2
    STATUS_CHOICES = (
        (available, 'موجود'),
        (unavailable, 'ناموجود')
    )
    status = models.IntegerField('وضعیت', choices=STATUS_CHOICES)

    man = models.BooleanField(_('Man'), default=False)
    women = models.BooleanField(_('Women'), default=False)

    iranian = 1
    foreign = 2
    MAKING_CHOICES = (
        (iranian, 'ایرانی'),
        (foreign, 'خارجی')
    )
    making = models.IntegerField('ساخت', choices=MAKING_CHOICES)

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )
    variant = models.CharField('مشخصات', max_length=10, choices=VARIANTS, default='Size-Color')
    
    hits = models.ManyToManyField(IpAddress, blank=True, related_name='hits', verbose_name='بازدید ها')
    
    created = models.DateTimeField('ایجاد', auto_now_add=True)
    updated = models.DateTimeField('به روز رسانی', auto_now=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        return format_html('<img src="{}" height="50" width="75" style="border-radius: 5px" />'.format(self.image.url))

    image_tag.short_description = 'عکس'

    def get_absolute_url(self):
        return reverse('home:details', args=[str(self.id), self.slug])


class Discount(models.Model):
    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیفات'
    title = models.CharField('عنوان', max_length=200)
    product = models.ManyToManyField(Product, related_name='discount', verbose_name=_('Product'))
    discount = models.IntegerField('تخفیف')
    valid_from = models.DateTimeField(_('From'))
    valid_to = models.DateTimeField(_('To'))
    active = models.BooleanField(_('Active?'), default=True)

    def jvalid_from(self):
        return jalali_converter(self.valid_from)
    jvalid_from.short_description = 'از تاریخ'

    def jvalid_to(self):
        return jalali_converter(self.valid_to)
    jvalid_to.short_description = 'تا تاریخ'

    def save(self, *args, **kwargs):
        if timezone.now() < self.valid_from or timezone.now() > self.valid_to:
            self.active = False
        else:
            self.active = True    
        super(Discount, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Color(models.Model):
    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ'
    name = models.CharField('رنگ', max_length=20)
    code = models.CharField('کد', max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return format_html('<p style="background-color:{}">Color</p>'.format(self.code))
        else:
            return ""
    color_tag.short_description = 'رنگ'


class Size(models.Model):
    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز'
    name = models.CharField('سایز', max_length=20)
    code = models.CharField('کد', max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Images(models.Model):
    class Meta:
        verbose_name = 'عکس'
        verbose_name_plural = 'عکس'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    title = models.CharField('عنوان', max_length=50, blank=True)
    image = models.ImageField('عکس', blank=True, upload_to='katoni_images/')

    def __str__(self):
        return self.title


class Variants(models.Model):
    class Meta:
        verbose_name = 'مشخصات'
        verbose_name_plural = 'مشخصات'
    title = models.CharField('عنوان', max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='محصول')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True, verbose_name='رنگ')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True, verbose_name='سایز')
    image_id = models.IntegerField('کد عکس', blank=True, null=True, default=0)
    price = models.IntegerField('قیمت', default=0)
    number = models.PositiveIntegerField('تعداد', default=1)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return format_html('<img src="{}" height="50" />'.format(img.image.url))
        else:
            return ""


class Comment(models.Model):
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    comment = models.TextField('نظر')
    active = models.BooleanField('فعال', default=True)
    created = models.DateTimeField('ایجاد', auto_now_add=True)
    updated = models.DateTimeField('به روز رسانی', auto_now=True)

    def __str__(self):
        return self.user.first_name

    def jcreated(self):
        return jalali_converter(self.created)
    jcreated.short_description = 'تاریخ سفارش'


class Slider(models.Model):
    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر'
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField('عکس', upload_to='katoni_images/sliders')

    def __str__(self):
        return self.product.name