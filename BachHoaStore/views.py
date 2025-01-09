from django.shortcuts import render
from product.models import Product
from product.utils import format_currency
from cart.models import Cart, CartItem
from cart.views import _generate_cart_id as _cart_id
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from user.models import User
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
        product.price_sale = format_currency(product.price + product.price * Decimal(0.15))
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
def format_currency(amount):
    formatted_amount = f"{amount:,.0f}đ"
    return formatted_amount.replace(",", ".")

def home_search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(product_name__icontains=query, is_available=True)
    
    for product in products:
        product.price_sale = format_currency(product.price + product.price * Decimal(0.15))
        product.price = format_currency(product.price)
    
    context = {
        'products': products,
        'query': query,
    }
    
    return render(request, 'search-result.html', context)
@login_required(login_url='login')
def place_order(request):
    try:
        cart_id = _cart_id(request)
        cart = Cart.objects.get(cart_id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    except Cart.DoesNotExist:
        cart_items = []

    total = sum(item.product.price * item.quantity for item in cart_items)
    tax = total * Decimal(0.02)  # Giả sử thuế là 2%
    grand_total = total + tax
    user = request.user
    user_address = user.default_address if user.default_address else None

    context = {
        'cart_items': cart_items,
        'total': format_currency(total),
        'tax': format_currency(tax),
        'grand_total': format_currency(grand_total),
        'user_address': user_address,
        'cart_id': cart_id
    }
    return render(request, 'place-order.html', context)
@login_required(login_url='login')
def order_complete(request):
    return render(request, 'order_complete.html')


@csrf_exempt
def save_user_address(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        data = json.loads(request.body)  # Parse JSON data
        district = data.get('district')
        ward = data.get('ward')
        street_address = data.get('street_address')

        if not district or not ward or not street_address:
            return JsonResponse({'error': 'Incomplete address data'}, status=400)

        # Update user's address
        user = request.user
        user.address = f"{street_address}, {ward}, {district}"
        user.city = 'TPHCM'
        user.save()

        return JsonResponse({'message': 'Address saved successfully!'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
