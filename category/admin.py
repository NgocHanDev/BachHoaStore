from django.contrib import admin
from .models import Category, SubCategory

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'description')
    prepopulated_fields = {'slug': ('category_name',)}

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category_name', 'slug', 'category')
    prepopulated_fields = {'slug': ('sub_category_name',)}


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)