from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'registration'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.user_profile, name='profile'),
    path('edit_profile/', views.user_editprofile, name='edit_profile'),
    path('password_change/', views.password_change, name='password_change'),
    path('orders/', views.user_orders, name='orders'),
    path('orderdetails/<int:id>/', views.user_orderdetails, name='orderdetails'),
    path('panel-admin/', views.adminpnl, name='adminpnl'),

    # reset_password_urls
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password_reset_complete/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
