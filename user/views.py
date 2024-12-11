from django.shortcuts import render
from .form  import RegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        print('POST')
    form = RegisterForm();
    
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context=context)

def login(request):
    return render(request, 'user/login.html')

def logout(request):
    return render(request, 'user/login.html')