from django.db import models
from category.models import SubCategory
from unidecode import unidecode
from django.utils.text import slugify
    
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    description = models.TextField(max_length=255, blank=True)
    images = models.ImageField(upload_to='photos/products')
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    sub_cate = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    
        
    def __str__(self):
        return self.product_name
    
class Attribute(models.Model):
    key = models.CharField(max_length=100, default=None)
    value = models.CharField(max_length=255, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"product: {self.product.product_name}, key: {self.key}"