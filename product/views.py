from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,ReviewRating, Reply
from .utils import format_currency
from category.models import Category, SubCategory
from cart.models import Cart, CartItem
from cart.views import _generate_cart_id as _cart_id
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db.models import Avg, Count
from .forms import ReviewForm, ReplyForm
from django.http import JsonResponse
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from decimal import Decimal

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
        product.price_sale = format_currency(product.price + product.price * Decimal(0.15))
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
    recommended_products = []
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
    #recommendation
    database = 'db.sqlite3'
    try:
        conn = sqlite3.connect(database)
        query = "SELECT product_product.slug,product_product.id, product_product.product_name, category_name, sub_category_name FROM product_product JOIN category_category ON product_product.cate_id = category_category.id JOIN category_subcategory ON product_product.sub_cate_id = category_subcategory.id"
        df = pd.read_sql(query, conn)
    except Exception as e:
        print(e)
        df = pd.DataFrame()  # Empty DataFrame in case of error
    finally:
        if conn:
            conn.close()

    if not df.empty:
        features = ['product_name','category_name', 'sub_category_name']

        def combined_features(row):
            return str(row['product_name']) + 'category_' + str(row['category_name']) + ' subcategory_' + str(row['sub_category_name'])

        df['combined_features'] = df.apply(combined_features, axis=1)

        tf = TfidfVectorizer()
        tfMatrix = tf.fit_transform(df['combined_features'])
        similar = cosine_similarity(tfMatrix)

        # Find the index of the selected product
        selected_product_index = df[df['slug'] == product_slug].index[0]

        # Get similarity scores for the selected product
        similar_products = list(enumerate(similar[selected_product_index]))
        similar_products = [
        (index, score) for index, score in similar_products 
        if score > 0.2 and index != selected_product_index
    ]
        # Sort the products based on similarity scores
        similar_products = sorted(similar_products, key=lambda x: x[1], reverse=True)
        # Exclude the selected product itself and get top 5 recommendations
        similar_products = similar_products[1:7]

        # Get the recommended products
        recommended_products = [Product.objects.get(id=df.iloc[i[0]]['id']) for i in similar_products]
    for product in recommended_products:
        product.in_cart = False
        product.price_sale = format_currency(product.price + product.price * Decimal(0.15))
        product.price = format_currency(product.price)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.filter(cart=cart, product=product)
            if cart_item.exists():
                product.in_cart = True
        except Cart.DoesNotExist:
            pass
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'recommended_products': recommended_products,
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
            rating = form.cleaned_data.get('rating')
            review_text = form.cleaned_data.get('review')
            if not rating:
                messages.error(request, 'Hãy đánh giá sao!')
            elif not review_text:
                messages.error(request, 'Hãy viết đánh giá!')
            else:
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

def edit_review(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đánh giá của bạn đã được cập nhật.')
            return redirect('product_detail.html', category_slug=review.product.cate.slug, sub_category_slug=review.product.sub_cate.slug, product_slug=review.product.slug)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'product/edit_review.html', {'form': form, 'review': review})

def delete_review(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, 'Đánh giá của bạn đã được xóa.')
    return redirect('product_detail', category_slug=review.product.cate.slug, sub_category_slug=review.product.sub_cate.slug, product_slug=product_slug)

def like_review(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id)
    if request.user in review.likes.all():
        review.likes.remove(request.user)
    else:
        review.likes.add(request.user)
        review.dislikes.remove(request.user)  # Hủy bỏ "Không thích" nếu đã chọn
    return redirect(request.META.get('HTTP_REFERER'))

def dislike_review(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id)
    if request.user in review.dislikes.all():
        review.dislikes.remove(request.user)
    else:
        review.dislikes.add(request.user)
        review.likes.remove(request.user)  # Hủy bỏ "Thích" nếu đã chọn
    return redirect(request.META.get('HTTP_REFERER'))

def reply_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(ReviewRating, id=review_id)
        reply_text = request.POST.get('reply')
        if reply_text:
            reply = Reply.objects.create(
                review=review,
                user=request.user,
                reply=reply_text
            )
            messages.success(request, 'Phản hồi của bạn đã được gửi.')
    return redirect(request.META.get('HTTP_REFERER'))

def edit_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id, user=request.user)
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            messages.success(request, 'Phản hồi của bạn đã được cập nhật.')
            return redirect('product_detail.html', category_slug=reply.review.product.cate.slug, sub_category_slug=reply.review.product.sub_cate.slug, product_slug=reply.review.product.slug)
    else:
        form = ReplyForm(instance=reply)
    return render(request, 'product/edit_reply.html', {'form': form})

def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id, user=request.user)
    product_slug = reply.review.product.slug
    reply.delete()
    messages.success(request, 'Phản hồi của bạn đã được xóa.')
    return redirect('product_detail', category_slug=reply.review.product.cate.slug, sub_category_slug=reply.review.product.sub_cate.slug, product_slug=product_slug)