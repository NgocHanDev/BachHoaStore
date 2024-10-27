from django.urls import path
from . import views

urlpatterns = [
    path('', views.product, name='product'), 
    path('<slug:category_slug>/', views.product, name='product_by_category'),
    path('<slug:category_slug>/<slug:sub_category_slug>/', views.product, name='product_by_category_and_sub_category'),
]
