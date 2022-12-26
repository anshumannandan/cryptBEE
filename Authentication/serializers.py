from rest_framework.serializers import Serializer, ModelSerializer, EmailField, CharField, BooleanField, IntegerField, UUIDField
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Two_Factor_Verification, PAN_Verification, User, Two_Factor_OTP
from .utils import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password


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
    email = EmailField()

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
    email = EmailField()
    otp = IntegerField()

    def validate(self, data):
        user = User.objects.get(email = data['email'])
        response = validateOTP(user, data['otp'])
        if response == 'OK':
            return data
        raise ValidationError(response)

    def create(self, validated_data):
        return validated_data


class ResetPasswordSerializer(Serializer):
    email = EmailField(write_only = True)
    otp = IntegerField(write_only = True)
    password = CharField()

    def validate(self, data):
        otpresponse = validateOTP(self.instance, data['otp'])
        if not otpresponse == 'OK' :
            raise ValidationError({'message' : 'unauthorised access'})
        passresponse = validatePASS(data['password'], self.instance.email)
        if not passresponse == 'OK':
            raise ValidationError(passresponse)
        otpresponse = validateOTP(self.instance, data['otp'], resetpass = True)
        return data

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance


class SendLINKEmailSerializer(Serializer):
    email = EmailField()
    password = CharField()

    def validate_email(self, email):
        if User.objects.filter(email = email).exists():
            raise ValidationError({'message' : 'User with this email already exists'})
        return email

    def validate_password(self, password):
        response = validatePASS(password)
        if response == 'OK':
            return password
        raise ValidationError(response)


class VerifyLINKEmailSerializer(Serializer):
    email = EmailField(required = True)
    token = UUIDField(required = True)

    def validate(self, data):
        email, token = data['email'], data['token']
        object = SignUpUser.objects.filter(email = email)
        if not object.exists():
            raise ValidationError({'message' : 'Invalid Email'})
        tempuser = object[0]
        if not token == tempuser.token:
            raise ValidationError({'message' : 'Invalid Token'})
        if tempuser.token_generated_at + timedelta(minutes=15) < timezone.now():
            tempuser.delete()
            raise ValidationError({'message' : 'Link Expired'})
        if tempuser.is_verified:
            raise ValidationError({'message' : 'Link already used'})
        return data | {"object" : tempuser}

    def create(self, validated_data):
        tempuser = validated_data['object']
        tempuser.is_verified = True
        tempuser.save()
        newuser = User(
            email = tempuser.email,
            name = tempuser.email.split("@")[0]
        )
        newuser.set_password(tempuser.password)
        newuser.save()
        return validated_data


class CheckVerificationSerializer(Serializer):
    is_verified = BooleanField(read_only = True, default = False)
    email = EmailField(write_only = True)
    password = CharField(write_only = True)
    access = CharField(read_only = True)
    refresh = CharField(read_only = True)

    def validate(self, data):
        object = SignUpUser.objects.filter(email = data['email'], password = data['password'])
        if not object.exists():
            raise ValidationError({'message' : 'Unauthorized Access'})
        if object[0].is_verified:
            data['is_verified'] = True
            user = authenticate(email=data['email'], password=data['password'])
            data['refresh'] = user.refresh
            data['access'] = user.access
            object[0].delete()
        return data

    def create(self, validated_data):
        return validated_data


class VerifyPANSerializer(ModelSerializer):
    email = EmailField()
    name = CharField()
    
    class Meta:
        model = PAN_Verification
        fields = ['email', 'pan_number', 'name']

    def validate_email(self, email):
        user = User.objects.filter(email = email)
        if user.exists():
            return user[0]
        raise ValidationError({'message' : 'User with provided Email does not exist'})
    
    def create(self, validated_data):
        holder = User.objects.get(email = validated_data['email'])
        PAN_Verification(
            user = holder,
            pan_number = validated_data['pan_number']
        ).save()
        holder.name = validated_data['name']
        holder.save()
        return validated_data