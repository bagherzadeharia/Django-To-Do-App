from django.urls import path
from accounts.views import *
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('signup', UserLoginView.as_view(), name='signup'),
]