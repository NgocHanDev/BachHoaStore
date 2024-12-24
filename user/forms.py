from django import forms
from .models import User

class AddressForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['address', 'city', 'default_address']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'default_address': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }