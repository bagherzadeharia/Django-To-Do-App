from accounts.api.v1.views import *
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = 'api-v1'

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='registration'),
    path('token/login/', DjangoAuthTokenView.as_view(), name='token-login'),
    path('token/logout/', DjangoAuthTokenDiscardView.as_view(), name='token-logout'),
    path('jwt/create/', SimpleJWTCreateView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    path('verification/confirm/<str:token>', UserVerificationConfirmView.as_view(), name='verification-confirm'),
    path('verification/resend/', UserVerificationEmailResendView.as_view(), name='verification-resend'),
]
