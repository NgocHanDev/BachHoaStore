from django.contrib import admin
from .models import Product, Attribute, ReviewRating

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'slug', 'images', 'is_available', 'created_date', 'modified_date', 'sub_cate')
    prepopulated_fields = {'slug': ('product_name',)}

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value')
    ordering = ('product',)

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'user', 'subject', 'review', 'rating', 'ip', 
        'status', 'flagged_as_spam', 'created_at', 'updated_at', 'image', 'video'
    )
    list_filter = ('status', 'flagged_as_spam', 'created_at')
    ordering = ('product', 'user', 'rating', 'created_at')
    actions = ['approve_reviews', 'mark_as_spam']

    # duyệt đánh giá
    def approve_reviews(self, request, queryset):
        queryset.update(flagged_as_spam=False, status=True)
        self.message_user(request, "Các đánh giá được chọn đã được duyệt thành công.")
    approve_reviews.short_description = "Duyệt các đánh giá được chọn"

    # gắn cờ spam
    def mark_as_spam(self, request, queryset):
        queryset.update(flagged_as_spam=True, status=False)
        self.message_user(request, "Các đánh giá được chọn đã bị gắn cờ spam.")
    mark_as_spam.short_description = "Gắn cờ spam cho các đánh giá được chọn"


admin.site.register(Product, ProductAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
