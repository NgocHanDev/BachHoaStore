from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating', 'image', 'video']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review', 'image', 'video']