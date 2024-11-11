from django.shortcuts import render, get_object_or_404
from .models import Product
from .utils import format_currency
from category.models import Category, SubCategory
from cart.models import Cart, CartItem
from cart.views import _generate_cart_id as _cart_id

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
        product.in_cart = False
        product.price_sale = format_currency(product.price + product.price * 0.15)
        product.price = format_currency(product.price)
        try:
            # cart = get_object_or_404(Cart, cart_id = _cart_id(request))
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.filter(cart = cart, product = product)
            if cart_item.exists():
                product.in_cart = True
        except Cart.DoesNotExist:
            pass
    
    context = {
        'products': products,
        'categories': list_all_category,
        'sub_categories': list_all_sub_category,
        'current_category': category_slug,
        'current_sub_category': sub_category_slug
    }
    
    return render(request, 'product/product.html', context)


def product_detail(request,category_slug=None, sub_category_slug=None, product_slug=None):
    in_cart = False
    try:
        single_product = Product.objects.get(cate__slug = category_slug, sub_cate__slug = sub_category_slug, slug = product_slug)
        # check if product is in cart
        # cart = get_object_or_404(Cart, cart_id = _cart_id(request))
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.filter(cart = cart, product = single_product)
        if cart_item.exists():
            in_cart = True
    except Exception as e:
        pass
    single_product.price = format_currency(single_product.price)
    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }
    
    return render(request, 'product/product_detail.html', context=  context)