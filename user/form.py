from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter your password...',
        'class': 'form-control'
    }))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter your password again...',
        'class': 'form-control'
    }))   
    phone_number = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your phone number...',
    }))
    email = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your email...',
    }))
    full_name = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter your full name...',
    }))
    class Meta:
        model = User
        fields = ['phone_number', 'email', 'full_name', 'password']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'