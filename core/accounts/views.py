from accounts.forms import UserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo:list")