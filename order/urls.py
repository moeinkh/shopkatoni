from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('orderproduct/', views.order_create, name='orderproduct'),
]