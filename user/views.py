from django.shortcuts import render, redirect
from .form  import RegisterForm
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

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