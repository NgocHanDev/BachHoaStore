from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.category_name
    
class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "sub category"
        verbose_name_plural = "sub_categories"
        
    def __str__(self):
        return self.sub_category_name