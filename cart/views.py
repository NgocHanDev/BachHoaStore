from django.shortcuts import get_object_or_404, render 
from product.models import Product
from .models import Cart, CartItem
from django.shortcuts import redirect
from product.utils import format_currency
from decimal import Decimal

# Create your views here.

def _generate_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def cart(request, total = 0, quantity = 0, cart_items = None):
    tax = {"percent": Decimal('0.02'), "total": Decimal('0')}
    root_price = Decimal('0')
    try: 
        cart = Cart.objects.get(cart_id = _generate_cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            root_price += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity 
            tax['total'] = root_price * tax['percent']
        
        total = root_price + tax['total']
        tax['total'] = format_currency(tax['total'])
        tax['percent'] = int(tax['percent'] * 100)
    except Cart.DoesNotExist:
        pass
    
    context = {
        'root_price': format_currency(root_price),
        'total': format_currency(total),
        'tax': tax,
        'cart_id': cart.cart_id,
        'quantity': quantity,
        'cart_items': cart_items
    }
    
    return render(request, 'cart/cart.html', context)

def empty_cart(request):
    print('empty cart')
    try:
        cart = Cart.objects.get(cart_id = _generate_cart_id(request))
        cart.delete()
    except Cart.DoesNotExist:
        pass
    return redirect(request.META['HTTP_REFERER'])
    

def remove_cart_all(request, product_id):
    cart = get_object_or_404(Cart, cart_id = _generate_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    try:
        cart_item = CartItem.objects.get(cart = cart, product = product)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect(request.META['HTTP_REFERER'])

def remove_cart(request, product_id):
    cart = get_object_or_404(Cart, cart_id = _generate_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    try:
        cart_item = CartItem.objects.get(cart = cart, product = product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect(request.META['HTTP_REFERER'])
    

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_generate_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _generate_cart_id(request)
        )
        cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect(request.META['HTTP_REFERER'])

def get_cart_total(request):
    total = 0
    try:
        cart = Cart.objects.get(cart_id = _generate_cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
    except Cart.DoesNotExist:
        pass
    return total