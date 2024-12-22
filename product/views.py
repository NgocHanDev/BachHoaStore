from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,ReviewRating
from .utils import format_currency
from category.models import Category, SubCategory
from cart.models import Cart, CartItem
from cart.views import _generate_cart_id as _cart_id
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db.models import Avg, Count

def product(request, category_slug=None, sub_category_slug=None):
    categories = None
    sub_categories = None
    products = None

    if category_slug is not None:
        if sub_category_slug is not None:
            categories = get_object_or_404(Category, slug=category_slug)
            sub_categories = get_object_or_404(SubCategory, slug=sub_category_slug)
            products = Product.objects.filter(cate=categories, sub_cate=sub_categories, is_available=True)
        else:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(cate=categories, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    list_all_category = Category.objects.all()
    list_all_sub_category = SubCategory.objects.all()

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 6)  # Hiển thị 6 sản phẩm mỗi trang
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Định dạng giá và kiểm tra giỏ hàng
    for product in products:
        product.in_cart = False
        product.price_sale = format_currency(product.price + product.price * 0.15)
        product.price = format_currency(product.price)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.filter(cart=cart, product=product)
            if cart_item.exists():
                product.in_cart = True
        except Cart.DoesNotExist:
            pass

    context = {
        'products': products,
        'categories': list_all_category,
        'sub_categories': list_all_sub_category,
        'current_category': category_slug,
        'current_sub_category': sub_category_slug,
    }

    return render(request, 'product/product.html', context)


def product_detail(request, category_slug=None, sub_category_slug=None, product_slug=None):
    in_cart = False
    reviews = []
    average_rating = 0
    review_count = 0

    try:
        single_product = Product.objects.get(
            cate__slug=category_slug, sub_cate__slug=sub_category_slug, slug=product_slug
        )
        
        # Kiểm tra sản phẩm có trong giỏ hàng không
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.filter(cart=cart, product=single_product)
        if cart_item.exists():
            in_cart = True
        
        # Lấy đánh giá
        reviews = ReviewRating.objects.filter(product=single_product, status=True)
        review_count = reviews.count()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    except Exception as e:
        pass

    single_product.price = format_currency(single_product.price)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_count': review_count,
    }
    return render(request, 'product/product_detail.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                review = ReviewRating.objects.get(user=request.user, product_id=product_id)
                form = ReviewForm(request.POST, request.FILES, instance=review)
            except ReviewRating.DoesNotExist:
                review = form.save(commit=False)
                review.product_id = product_id
                review.user = request.user
                review.ip = request.META.get('REMOTE_ADDR')
            review.save()
            messages.success(request, 'Cảm ơn bạn! Đánh giá của bạn đã được gửi.')
        else:
            messages.error(request, 'Có lỗi xảy ra. Vui lòng kiểm tra lại.')
        return redirect(url)