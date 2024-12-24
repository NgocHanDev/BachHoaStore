from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['rating', 'review', 'image', 'video']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review', 'image', 'video']