from django.shortcuts import render
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from product.models import Product, Holiday, Category

def calculate_discount(product):
    now = datetime.now()
    time_to_expiry = product.expiry_date - now.date()
    discount = Decimal(0)

    if product.cate.category_name in ['Thịt', 'Cá', 'Hải sản'] and 'Trứng' not in product.product_name:
        if time_to_expiry <= timedelta(hours=6):
            discount = Decimal(0.4)
        if time_to_expiry <= timedelta(hours=3):
            discount = Decimal(0.6)
    elif product.cate.category_name in ['Rau', 'Củ', 'Nấm', 'Trái cây']:
        if time_to_expiry <= timedelta(hours=6):
            discount = Decimal(0.4)
        if time_to_expiry <= timedelta(hours=3):
            discount = Decimal(0.6)
    elif product.cate.category_name in ['Dầu ăn', 'Nước mắm', 'Gia vị']:
        if time_to_expiry <= timedelta(days=6):
            discount = Decimal(0.4)
        if time_to_expiry <= timedelta(days=3):
            discount = Decimal(0.6)

    return discount

def promotions(request):
    now = datetime.now().date()
    
    # Lấy các sản phẩm thực tế từ cơ sở dữ liệu
    expiring_soon_products = Product.objects.filter(expiry_date__isnull=False)
    holiday_promotion_products = Product.objects.filter(is_holiday_promotion=True, holidays__date=now)

    # Nếu không có sản phẩm thực tế, thêm các sản phẩm mẫu
    if not expiring_soon_products.exists():
        expiring_soon_products = [
            Product(
                id=1,
                product_name="Thịt Bò",
                price=Decimal(100000),
                expiry_date=now + timedelta(hours=5),
                images="https://i.postimg.cc/zD2q3w5P/th-t-b.jpg",
                cate=Category(category_name="Thịt"),
            ),
            Product(
                id=2,
                product_name="Cá Hồi",
                price=Decimal(150000),
                expiry_date=now + timedelta(hours=2),
                images="https://i.postimg.cc/jS5g2Nxv/ca-hoi-na-uy-1.jpg",
                cate=Category(category_name="Cá"),
            ),
        ]

    if not holiday_promotion_products.exists():
        holiday_promotion_products = [
            Product(
                id=3,
                product_name="Nước Mắm Vị Ngư",
                price=Decimal(50000),
                is_holiday_promotion=True,
                holiday_promotion_type="discount10",
                images="https://i.postimg.cc/gjLcGrw0/z4180644297530-3761dde08797955656b826db4c27696f.jpg",
                cate=Category(category_name="Gia vị"),
            ),
            Product(
                id=4,
                product_name="Dầu Ăn Meizan",
                price=Decimal(70000),
                is_holiday_promotion=True,
                holiday_promotion_type="buy2get1",
                images="https://i.postimg.cc/Wz7VNrNT/dauan.jpg",
                cate=Category(category_name="Dầu ăn"),
            ),
        ]

    for product in expiring_soon_products:
        product.discount = calculate_discount(product)
        product.discounted_price = (product.price * (Decimal(1) - product.discount)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        product.discount_percentage = product.discount * 100  # Thêm thông tin giảm giá phần trăm

    for product in holiday_promotion_products:
        if product.holiday_promotion_type == 'discount10':
            product.discount = Decimal(0.1)
            product.discounted_price = (product.price * (Decimal(1) - product.discount)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        elif product.holiday_promotion_type == 'buy2get1':
            product.discount = None
            product.discounted_price = None

    context = {
        'expiring_soon_products': expiring_soon_products,
        'holiday_promotion_products': holiday_promotion_products,
    }
    return render(request, 'product/promotions.html', context)
