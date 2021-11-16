from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('profile/', views.user_profile, name='profile'),
    path('edit_profile/', views.user_editprofile, name='edit_profile'),
    path('orders/', views.user_orders, name='orders'),
    path('orderdetails/<int:id>/', views.user_orderdetails, name='orderdetails'),
    path('panel-admin/', views.adminpnl, name='adminpnl'),
]
