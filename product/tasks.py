from celery import shared_task
from datetime import date
from .models import Product

@shared_task
def check_and_update_expired_products():
    # Lọc các sản phẩm có ngày hết hạn đã qua và vẫn đang được đánh dấu là "is_available"
    expired_products = Product.objects.filter(expiry_date__lt=date.today(), is_available=True)
    
    # Cập nhật các sản phẩm hết hạn thành không khả dụng
    count = expired_products.update(is_available=False)
    print(f"{count} sản phẩm đã hết hạn!")
    return f"{count} sản phẩm đã hết hạn!"
