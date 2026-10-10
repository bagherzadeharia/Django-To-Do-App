import jwt
from django.conf import settings
from accounts.models import User
from rest_framework import status
from mail_templated import EmailMessage
from rest_framework.views import APIView
from accounts.api.v1.serializers import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

class RegistrationAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def _get_token(self, user):
        token = RefreshToken.for_user(user)
        return token.access_token

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            createdUser = get_object_or_404(User, email=serializer.validated_data['email'])
            token = self._get_token(createdUser)
            activationEmail = EmailMessage(
                'email/verification-email.tpl',
                {
                    'token': token,
                },
                'admin@todo.app',
                [createdUser.email,],
            )
            activationEmail.send()
            return Response({"detail": "User Has Been Registered Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    'detail': list(serializer.errors)
                }
            )

class ChangePasswordAPIView(GenericAPIView):
    model = User
    authorization_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response(
                    {
                        "old_password": ["Wrong Password"],
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                self.object.set_password(serializer.data.get('new_password'))
                self.object.save()
                response = {
                    'status': 'Success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password Updated Successfully',
                    'data': []
                }
                return Response(response)

        else:
            return Response(
                {
                    'detail': list(serializer.errors)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class DjangoAuthTokenView(GenericAPIView):
    serializer_class = DjangoAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(
                user=user
            )
            return Response(
                {
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email,
                    'full_name': user.full_name,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'detail': list(serializer.errors)
                }
            )

class DjangoAuthTokenDiscardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        self.request.user.auth_token.delete()
        return Response(
            {
                'detail': 'Token Deleted',
            },
            status=status.HTTP_204_NO_CONTENT,
        )

class SimpleJWTCreateView(TokenObtainPairView):
    serializer_class = SimpleJWTSerializer

class UserVerificationConfirmView(APIView):
    def get(self, request, token, *args, **kwargs):
        print(args)
        print(kwargs)
        try:
            decodedToken = AccessToken(token)
            userID = decodedToken["user_id"]
        except TokenError as e:
            print(e.args)
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(
            pk=userID
        )

        if user.is_verified:
            return Response(
                {
                    'detail': 'User has already been '
                },
                status=status.HTTP_200_OK
            )
        else:
            user.is_verified=True
            user.save()
            return Response(
                {
                    'detail': 'User has been verified & activated successfully'
                },
                status=status.HTTP_200_OK
            )

class UserVerificationEmailResendView(APIView):
    def get(self, request, token, *args, **kwargs):
        pass
