from django.urls import path
from . import views

urlpatterns = [
    path('', views.product, name='product'), 
    path('category/<slug:category_slug>/', views.product, name='product_by_category'),
    path('category/<slug:category_slug>/sub-category/<slug:sub_category_slug>/', views.product, name='product_by_category_and_sub_category'),
    path('category/<slug:category_slug>/sub-category/<slug:sub_category_slug>/product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),]
