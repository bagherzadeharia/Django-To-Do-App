from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="email")

class UserSignUpForm(forms.Form):
    email = forms.EmailField(label="email")
    full_name = forms.CharField(max_length=200)
    password = forms.CharField(max_length=255)