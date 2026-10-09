from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.generics import GenericAPIView

class UserRegisterAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def get(self, request, *args, **kwargs):
        return Response({"details": "User Has Been Registered Successfully"}, status=status.HTTP_200_OK)
