from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('addtoshop/<int:id>', views.addtoshop, name='addtoshop'),
    path('deletefromshop/<int:id>', views.deletefromshop, name='deletefromshop'),
    path('shopcart/', views.shopcart, name='shopcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
]