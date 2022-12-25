from rest_framework.serializers import Serializer, EmailField, CharField, BooleanField, IntegerField
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Two_Factor_Verification, PAN_Verification, User, Two_Factor_OTP
from .utils import *
from django.core.exceptions import ObjectDoesNotExist


class LoginSerializer(Serializer):
    email = EmailField(write_only = True)
    password = CharField(write_only = True)
    two_factor = BooleanField(read_only = True)
    refresh = CharField(read_only = True)
    access = CharField(read_only = True)
    pan_verify = BooleanField(read_only = True, default=False)

    def validate(self,data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise ValidationError('Invalid Credentials')
        if PAN_Verification.objects.filter(user = user).exists():
            data['pan_verify'] = True
        try:
            mobile = Two_Factor_Verification.objects.get(user = user)
            data['two_factor'] = True
            if resend_otp(user, twofactor = True):
                send_two_factor_otp(mobile)
            return data
        except ObjectDoesNotExist:
            data['refresh'] = user.refresh
            data['access'] = user.access
            data['two_factor'] = False
        return data

    def create(self, validated_data):
        return validated_data


class VerifyTwoFactorOTPSerializer(Serializer):
    email = EmailField(write_only = True)
    otp = IntegerField(write_only = True)
    refresh = CharField(read_only = True)
    access = CharField(read_only = True)

    def validate(self, data):
        user = User.objects.get(email = data['email'])
        response = validateOTP(user, data['otp'], twofactor = True)
        if response == 'OK':
            data['refresh'] = user.refresh
            data['access'] = user.access
            return data
        raise ValidationError(response)

    def create(self, validated_data):
        return validated_data


class SendOTPEmailSerializer(Serializer):
    email = EmailField(write_only = True)

    def validate(self, data):
        try:
            user = User.objects.get(email = data['email'])
        except ObjectDoesNotExist:
            raise ValidationError({"message" : "No such account exists"})
        if resend_otp(user):
            send_email_otp(user)
        return data

    def create(self, validated_data):
        return validated_data


class VerifyOTPEmailSerializer(Serializer):
    email = EmailField(write_only = True)
    otp = IntegerField(write_only = True)

    def validate(self, data):
        user = User.objects.get(email = data['email'])
        response = validateOTP(user, data['otp'])
        if response == 'OK':
            return data
        raise ValidationError(response)

    def create(self, validated_data):
        return validated_data


class SendLINKEmailSerializer(Serializer):
    email = EmailField(write_only = True)

    def validate(self, data):
        return data

    def create(self, validated_data):
        return validated_data