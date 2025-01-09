from django.db import models

# Create your models here.
from django import forms
from user.models import User
from cart.models import Cart
class PaymentForm(forms.Form):

    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=100)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)
    
class Payment_VNPay(models.Model):
    order_id = models.IntegerField(default=0, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    order_desc = models.CharField(max_length=200, null=True, blank=True)
    vnp_TransactionNo = models.CharField(max_length=200, null = True, blank=True)
    vnp_ResponseCode = models.CharField(max_length=200, null=True, blank=True)

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=250, unique=False)  # Mã giao dịc
    phone_number = models.CharField(max_length=50, blank=True)
    desc = models.TextField(null=True, blank=True)  # Mô tả giao dịch
    order_id = models.IntegerField()  # Mã đơn hàng liên kết

    def __str__(self):
        return f"Transaction {self.transaction_id} - Order {self.order_id}"