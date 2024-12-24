from django.shortcuts import render, redirect
from .form  import RegisterForm
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import AddressForm
from .models import Order

# Create your views here.
def register(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            try:
                user = User.objects.create_user(phone_number, email, full_name, password)
                user.save()
                messages.success(request, 'Đăng ký thành công!')
                return redirect('register')
            except ValueError as e:
                messages.error(request, str(e)) 
                return redirect('register')
    else:
        form = RegisterForm()
    context = {
        'form':form
    }
    
    return render(request, 'user/register.html', context=context)

def login(request):
    
    if request.method == 'POST':
        phone_number= request.POST['phone_number']
        password = request.POST['password']

        user = auth.authenticate(phone_number = phone_number, password = password)
        
        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'Bạn đã đăng nhập thành công!')
            return redirect('home')
        else:
            messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu')
            return redirect('login')
    return render(request, 'user/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Đăng xuất thành công!')
    return render(request, 'user/login.html')

def forgot_password(request):
    return render(request, 'user/forgot-password.html')
def profile(request):
    return render(request, 'user/profile.html')

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AddressForm(instance=user)
    
    # Lấy các đơn hàng của người dùng hiện tại
    orders = Order.objects.filter(user=user)
    
    # Dữ liệu giả cho các đơn hàng đang giao và trả hàng và hoàn tiền
    shipping_orders = [
        {
            'id': 3,
            'recipient_name': 'Le Thi C',
            'phone': '0123456789',
            'email': 'lethic@example.com',
            'address': '789 Đường DEF, Quận 3, TP.HCM',
            'payment_card_last4': '9101',
            'subtotal': 31000,
            'shipping_fee': 0,
            'total': 31000,
            'date_ordered': '2023-10-03',
            'status': 'shipping',
            'product': {
                'product_name': 'Cam sành 1 kg',
                'images': '../static/images/product/cam-sanh-loai-2-tui-1kg-202101271631264363.jpg',
                'price': 31000,
            }
        },
    ]
    
    return_orders = [
        {
            'id': 4,
            'recipient_name': 'Pham Van D',
            'phone': '0987654321',
            'email': 'phamvand@example.com',
            'address': '101 Đường GHI, Quận 4, TP.HCM',
            'postal_code': '700000',
            'payment_card_last4': '1121',
            'subtotal': 100000,
            'shipping_fee': 20000,
            'total': 120000,
            'date_ordered': '2023-10-04',
            'status': 'delivered',
            'return_reason': 'Sản phẩm bị lỗi',
            'product': {
                'product_name': 'Sản phẩm 2',
                'images': 'path/to/image2.jpg',
                'price': 100000,
            }
        },
    ]
    
    history_orders = [
        {
            'id': 1,
            'recipient_name': 'Nguyen Van A',
            'phone': '0123456789',
            'email': 'nguyenvana@example.com',
            'address': '123 Đường ABC, Quận 1, TP.HCM',
            'postal_code': '700000',
            'payment_card_last4': '1234',
            'subtotal': 500000,
            'shipping_fee': 30000,
            'total': 530000,
            'date_ordered': '2023-09-01',
            'status': 'delivered',
            'product': {
                'product_name': 'Sản phẩm 3',
                'images': 'path/to/image3.jpg',
                'price': 500000,
            }
        },
        {
            'id': 2,
            'recipient_name': 'Tran Thi B',
            'phone': '0987654321',
            'email': 'tranthib@example.com',
            'address': '456 Đường XYZ, Quận 2, TP.HCM',
            'postal_code': '700000',
            'payment_card_last4': '5678',
            'subtotal': 750000,
            'shipping_fee': 40000,
            'total': 790000,
            'date_ordered': '2023-09-15',
            'status': 'delivered',
            'product': {
                'product_name': 'Sản phẩm 4',
                'images': 'path/to/image4.jpg',
                'price': 750000,
            }
        },
    ]
    
    return render(request, 'user/profile.html', {
        'form': form,
        'user': user,
        'orders': orders,
        'shipping_orders': shipping_orders,
        'return_orders': return_orders,
        'history_orders': history_orders,
    })