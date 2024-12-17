from django.shortcuts import render
from product.models import Product
from product.utils import format_currency
from cart.models import Cart, CartItem
from cart.views import _generate_cart_id as _cart_id
from django.core.paginator import Paginator

def home(request):
    products_list = Product.objects.all().filter(is_available=True)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 8)  # Show 8 products per page

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    for product in products:
        product.price_sale = format_currency(product.price + product.price * 0.15)
        product.price = format_currency(product.price)
        product.in_cart = False
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.filter(cart=cart, product=product)
            if cart_item.exists():
                product.in_cart = True
        except Cart.DoesNotExist:
            pass

    context = {
        'products': products,
    }
    
    return render(request, 'home.html', context)
def format_currency(value):
    return "{:,.0f}".format(value)

def home_search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(product_name__icontains=query, is_available=True)
    
    for product in products:
        product.price_sale = format_currency(product.price + product.price * 0.15)
        product.price = format_currency(product.price)
    
    context = {
        'products': products,
        'query': query,
    }
    
    return render(request, 'search-result.html', context)
