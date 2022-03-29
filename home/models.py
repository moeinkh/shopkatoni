from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Setting(models.Model):
    class Meta:
        verbose_name = 'مشخصات'
        verbose_name_plural = 'مشخصات'

    title = models.CharField('عنوان', max_length=60)
    phone = models.CharField('تلفن', max_length=60)
    address = models.CharField('آدرس', max_length=60)
    description = models.TextField('توضیحات')
    email = models.CharField('ایمیل', max_length=60)
    telegram = models.CharField('تلگرام', max_length=60)
    instagram = models.CharField('اینستاگرام', max_length=60)
    icon = models.ImageField('لوگو', blank=True, upload_to='katoni_images/setting')
    created = models.DateTimeField('ایجاد', auto_now_add=True)
    updated = models.DateTimeField('به روز رسانی', auto_now=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها'

    title = models.CharField('عنوان', max_length=100)
    cover = models.ImageField('کاور', upload_to='katoni_images/articles')
    text = RichTextField('متن')

    created = models.DateTimeField('انتشار', auto_now_add=True)
    updated = models.DateTimeField('به روز رسانی', auto_now=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'
    
    first_name = models.CharField('نام', max_length=128)
    last_name = models.CharField('نام خانوادگی', max_length=128)
    email = models.EmailField('ایمیل')
    message = models.TextField('پیام')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

