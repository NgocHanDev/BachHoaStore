from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password=None):
        if not phone_number:
            raise ValueError('Vui lòng nhập số điện thoại!')

        if not email:
            raise ValueError('Vui lòng nhập email!')
        
        if self.model.objects.filter(phone_number=phone_number).exists():
            raise ValueError('Số điện thoại đã được đăng ký!')

        if self.model.objects.filter(email=email).exists():
            raise ValueError('Email đã được đăng ký!')
        
        user = self.model(
            phone_number = phone_number,
            email = self.normalize_email(email),
            full_name = full_name,
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, full_name, password=None):
        user = self.create_user(
            phone_number,
            email,
            full_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    avatar_url = models.URLField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    reward_points = models.IntegerField(default=0)
    default_address = models.CharField(max_length=255, blank=True, null=True)
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']
    
    objects = MyUserManager()

    def get_total_reward_points(self):
        orders = self.orders.all()  # Assuming a related name 'orders' for reverse relation
        total_amount = sum(order.total_amount for order in orders)
        return total_amount // 100

    def get_full_name(self):
        return self.full_name
    
    def __str__(self):
        return self.full_name

class Order(models.Model):
    STATUS_CHOICES = [
        ('delivered', 'Đã nhận hàng'),
        ('shipping', 'Đang giao'),
    ]
    
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(default='example@example.com')
    address = models.CharField(max_length=255, default='No address')
    payment_card_last4 = models.CharField(max_length=4)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='shipping')

    