from rest_framework import status
from rest_framework.views import APIView
from accounts.api.v1.serializers import *
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

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
