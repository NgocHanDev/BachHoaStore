from django.shortcuts import render
from product.models import Product
from product.utils import format_currency
from cart.models import Cart, CartItem
from cart.views import _generate_cart_id as _cart_id

def home(request):
    
    products = Product.objects.all().filter(is_available=True)
    for product in products:
        product.price_sale = format_currency(product.price + product.price * 0.15)
        product.price = format_currency(product.price)
        product.in_cart = False
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
    }
    
    return render(request,'home.html', context)