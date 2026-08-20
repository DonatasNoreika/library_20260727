from django.contrib.auth.models import User
from .models import BookReview, Profile
from django import forms

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['content']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']