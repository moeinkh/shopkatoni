from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('articles/', views.articles, name='articles'),
    path('details_articles/<int:id>', views.details_articles, name='details_articles'),
    path('details/<int:id>', views.details, name='details'),
    path('katoni/', views.katoni, name='katoni'),
    path('feminine/', views.feminine, name='feminine'),
    path('for_men/', views.for_men, name='for_men'),
    path('discounts/', views.discounts, name='discounts'),
    path('brand/<int:id>', views.brand, name='brand'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
]
