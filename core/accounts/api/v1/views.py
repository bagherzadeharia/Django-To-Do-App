from accounts.models import User
from rest_framework import status
from rest_framework.views import APIView
from accounts.api.v1.serializers import *
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

class RegistrationAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "User Has Been Registered Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': list(serializer.errors)}
            )

class ChangePasswordAPIView(GenericAPIView):
    model = User
    authorization_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
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
