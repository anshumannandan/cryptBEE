from rest_framework.generics import CreateAPIView
from .serializers import *
from rest_framework.permissions import AllowAny


class LoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer