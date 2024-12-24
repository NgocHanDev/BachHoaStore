from django.db import models
from category.models import SubCategory, Category
from django.urls import reverse
from user.models import User
from django.utils.text import slugify
    
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    description = models.TextField(max_length=255, blank=True)
    images = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    sub_cate = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    
        
    def __str__(self):
        return self.product_name
    def get_url(self):
        return reverse('product_detail', args=[self.cate.slug, self.sub_cate.slug, self.slug])
    
class Attribute(models.Model):
    key = models.CharField(max_length=100, default=None)
    value = models.CharField(max_length=255, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"product: {self.product.product_name}, key: {self.key}"
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    video = models.FileField(upload_to='reviews/', blank=True, null=True)
    
    likes = models.ManyToManyField(User, related_name='review_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='review_dislikes', blank=True)

    def like_review(self, user):
        if user not in self.likes.all():
            self.likes.add(user)
        if user in self.dislikes.all():
            self.dislikes.remove(user)

    def dislike_review(self, user):
        if user not in self.dislikes.all():
            self.dislikes.add(user)
        if user in self.likes.all():
            self.likes.remove(user)


    def __str__(self):
        return f"product: {self.product.product_name}, user: {self.user.username}, rating: {self.rating}"

class Reply(models.Model):
    review = models.ForeignKey(ReviewRating, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='reply_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='reply_dislikes', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.review.review[:20]}"