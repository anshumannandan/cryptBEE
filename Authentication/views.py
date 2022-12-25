from rest_framework.generics import CreateAPIView
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class LoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer


class VerifyTwoFactorOTPView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyTwoFactorOTPSerializer


class SendOTPEmailView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendOTPEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message' : 'OTP sent on email'}, status=status.HTTP_200_OK)


class VerifyOTPEmailView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message' : 'OTP Verified'}, status=status.HTTP_200_OK)


class SendLINKEmailView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendOTPEmailSerializer
