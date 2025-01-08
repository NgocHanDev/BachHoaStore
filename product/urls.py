from django.urls import path
from . import views

urlpatterns = [
    path('', views.product, name='product'), 
    path('category/<slug:category_slug>/', views.product, name='product_by_category'),
    path('category/<slug:category_slug>/sub-category/<slug:sub_category_slug>/', views.product, name='product_by_category_and_sub_category'),
    path('category/<slug:category_slug>/sub-category/<slug:sub_category_slug>/product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('like_review/<int:review_id>/', views.like_review, name='like_review'),
    path('dislike_review/<int:review_id>/', views.dislike_review, name='dislike_review'),
    path('reply_review/<int:review_id>/', views.reply_review, name='reply_review'),
    path('edit_reply/<int:reply_id>/', views.edit_reply, name='edit_reply'),
    path('delete_reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('approve_review/<int:review_id>/', views.approve_review, name='approve_review'),
    path('delete_review_spam/<int:review_id>/', views.delete_review_spam, name='delete_review_spam'),
]