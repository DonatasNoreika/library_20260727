from django.contrib.auth.models import User
from .models import BookReview, Profile, BookInstance
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


class BookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'reader', 'due_back', 'status']
        widgets = {'due_back': forms.DateInput(attrs={"type": "date"})}
