from accounts.models import User
from rest_framework import status
from rest_framework.views import APIView
from accounts.api.v1.serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

class RegistrationAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
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
