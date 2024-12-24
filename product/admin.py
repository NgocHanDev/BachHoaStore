from django.contrib import admin
from .models import Product, Attribute, ReviewRating



class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'slug', 'images', 'is_available', 'created_date', 'modified_date', 'sub_cate')
    prepopulated_fields = {'slug': ('product_name',)}
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value')
    ordering = ('product',)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'review', 'rating', 'ip', 'status', 'created_at', 'updated_at', 'image', 'video')
    ordering = ('product', 'user', 'rating', 'created_at')
# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Attribute,AttributeAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)