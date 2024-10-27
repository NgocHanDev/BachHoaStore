from django.shortcuts import render, get_object_or_404
from .models import Product
from .utils import format_currency
from category.models import Category, SubCategory

# Create your views here.
def product(request, category_slug=None, sub_category_slug=None):
    
    categories = None
    sub_categories = None
    products = None
    
    if category_slug != None:
        if sub_category_slug !=None:
            categories = get_object_or_404(Category,slug = category_slug)
            sub_categories = get_object_or_404(SubCategory,slug = sub_category_slug)
            products = Product.objects.all().filter(cate = categories, is_available = True, sub_cate = sub_categories)
        else:
            categories = get_object_or_404(Category,slug = category_slug)
            products = Product.objects.all().filter(cate = categories, is_available = True)
    else:
        products = Product.objects.all().filter(is_available = True)
    
    
    list_all_category = Category.objects.all()
    list_all_sub_category = SubCategory.objects.all()   
    for product in products:
        product.price_sale = format_currency(product.price + product.price * 0.15)
        product.price = format_currency(product.price)
    
    context = {
        'products': products,
        'categories': list_all_category,
        'sub_categories': list_all_sub_category,
        'current_category': category_slug,
        'current_sub_category': sub_category_slug
    }
    
    return render(request, 'product/product.html', context)