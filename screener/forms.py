from django import forms
from .models import WishList
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class WishListForm(forms.ModelForm):
  class Meta:
    model = WishList
    fields = ['wishlistname', 'tickers']

class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ('username','email','password1','password2')



