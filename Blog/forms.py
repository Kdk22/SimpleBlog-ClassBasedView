from django import forms
from .models import UserProfileInfo, Post
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta():
        model = User
        fields = ('username','password','email')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('portfolio_site','profile_pic')

class PostSearchForm(forms.Form):
    search_text = forms.CharField(
        required = False,
        label='Search title or categories!',
        widget=forms.TextInput(attrs={'placeholder': 'search here!'})
    )

