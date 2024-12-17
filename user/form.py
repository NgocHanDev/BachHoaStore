from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'nhập mật khẩu...',
        'class': 'form-control'
    }))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'nhập lại mật khẩu...',
        'class': 'form-control'
    }))   
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'nhập số điện thoại...',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'nhập email...',
    }))
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'nhập họ và tên...',
    }))
    class Meta:
        model = User
        fields = ['phone_number', 'email', 'full_name', 'password']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        
        if(password != repeat_password):
            raise forms.ValidationError("Mật khẩu không trùng khớp")

        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Số điện thoại đã được đăng ký!")
        
        if User.objects.filter(email=email).exists():
            raise   forms.ValidationError("Email đã được đăng ký!")
        
        return cleaned_data