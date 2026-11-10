from typing import override
from accounts.models import User
from django.urls import reverse_lazy
from django.contrib.auth import login
from mail_templated import EmailMessage
from accounts.api.utils import EmailThread
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from rest_framework.authtoken.models import Token
from accounts.forms import UserLoginForm, UserSignUpForm
from rest_framework_simplejwt.tokens import RefreshToken

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy("todo:list")

class UserSignUpView(FormView):
    model = User
    template_name = 'accounts/signup.html'
    form_class = UserSignUpForm
    success_url = reverse_lazy('todo:list')

    def _get_token(self, user):
        token = RefreshToken.for_user(user)
        return token.access_token

    def form_valid(self, form):
        user = User.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            full_name=form.cleaned_data['full_name'],
        )
        login(self.request, user)
        token = self._get_token(user)
        activationEmail = EmailMessage(
            'email/verification-email.tpl',
            {
                'token': token,
            },
            'admin@todo.app',
            [user.email,],
        )
        activationEmail.send()
        return super().form_valid(form)
