from accounts.views import *
from django.urls import path, include
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('api/v1/', include('accounts.api.v1.urls')),
]
