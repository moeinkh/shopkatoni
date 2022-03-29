from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_us, name='contact'),
    path('articles/', views.articles, name='articles'),
    path('details_articles/<int:id>', views.details_articles, name='details_articles'),
    path('details/<int:id>/<str:slug>/', views.details, name='details'),
    path('katoni/', views.katoni, name='katoni'),
    path('katoni/brand/<str:brand_slug>', views.katoni, name='katoni_brand'),
    path('katoni/category/<str:category_slug>', views.katoni, name='katoni_category'),
    path('feminine/', views.feminine, name='feminine'),
    path('for_men/', views.for_men, name='for_men'),
    path('discounts/', views.discounts, name='discounts'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
]
