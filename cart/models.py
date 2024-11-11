from django.db import models
from product.models  import Product
from product.utils import format_currency

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.product} ({self.quantity})"
    def sub_price(self):
        return format_currency(self.product.price * self.quantity)
    def price_format(self):
        return format_currency(self.product.price)