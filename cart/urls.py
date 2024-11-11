from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_all/<int:product_id>/', views.remove_cart_all, name='remove_cart_all'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    
]
