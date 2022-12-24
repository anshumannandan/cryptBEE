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