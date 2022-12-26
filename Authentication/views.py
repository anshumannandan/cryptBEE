from rest_framework.generics import CreateAPIView, UpdateAPIView
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
        print(serializer.data)
        return Response({'message' : 'OTP sent on email'}, status=status.HTTP_200_OK)


class VerifyOTPEmailView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message' : 'OTP Verified'}, status=status.HTTP_200_OK)


class ResetPasswordView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class  = ResetPasswordSerializer

    def get_object(self):
        email = self.request.data.get('email')
        return User.objects.get(email=email)

    def patch(self, request, *args, **kwargs):
        self.update(request,*args, **kwargs)
        return Response({'messsage':'Password changed successfully'}, status=status.HTTP_200_OK)


class SendLINKEmailView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SendLINKEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        tokenobject = SignUpUser.objects.filter(email = email)
        if tokenobject.exists():
            tokenobject = tokenobject[0]
            if tokenobject.token_generated_at + timedelta(minutes=1) > timezone.now():
                return Response({'messsage':'wait for a minute to send another request'}, status=status.HTTP_400_BAD_REQUEST)
            tokenobject.delete()
        send_email_token(serializer.data['password'], email)
        return Response({'messsage':'Email sent'}, status=status.HTTP_200_OK)


class VerifyLINKEmailView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = VerifyLINKEmailSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({'message' : 'Verified'}, status=status.HTTP_200_OK)


class CheckVerificationView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckVerificationSerializer


class VerifyPANView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyPANSerializer