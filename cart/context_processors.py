from .models import Cart, CartItem

def counter(request):
    count = 0
    
    if 'admin' in request.path:
        return {}
    try:
        cart_id = request.session.session_key
        cart = Cart.objects.get(cart_id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            count += item.quantity
    except Cart.DoesNotExist:
        pass
    
    return dict(cart_count=count)