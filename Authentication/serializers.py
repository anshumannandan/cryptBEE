from rest_framework.serializers import Serializer, ModelSerializer, EmailField, CharField, BooleanField, IntegerField, UUIDField
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Two_Factor_Verification, PAN_Verification, User
from .utils import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password


class LoginSerializer(Serializer):
    email = EmailField(write_only = True)
    password = CharField(write_only = True)
    two_factor = BooleanField(read_only = True)
    refresh = CharField(read_only = True)
    access = CharField(read_only = True)
    pan_verify = BooleanField(read_only = True)
    name = CharField(read_only = True)

    def validate(self,data):
        if not User.objects.filter(email = data['email']).exists():
            raise ValidationError({'message':'User not registered'})
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise ValidationError({'message':'Invalid Credentials'})
        try:
            mobile = Two_Factor_Verification.objects.get(user = user)
            data['two_factor'] = True
            if resend_otp(user, twofactor = True):
                send_two_factor_otp(mobile)
        except ObjectDoesNotExist:
            data['refresh'] = user.refresh
            data['access'] = user.access
            data['two_factor'] = False
            data['pan_verify'] = False
            if PAN_Verification.objects.filter(user = user).exists():
                data['pan_verify'] = True
            data['name'] = user.name
        return data


class VerifyTwoFactorOTPSerializer(Serializer):
    email = EmailField(write_only = True)
    otp = IntegerField(write_only = True)
    refresh = CharField(read_only = True)
    access = CharField(read_only = True)
    pan_verify = BooleanField(read_only = True)
    name = CharField(read_only = True)

    def validate(self, data):
        user = User.objects.filter(email = data['email'])
        if not user.exists():
            raise ValidationError({'message':'User not registered'})
        user = user[0]
        response = validateOTP(user, data['otp'], twofactoron = True)
        if response == 'OK':
            data['refresh'] = user.refresh
            data['access'] = user.access
            data['pan_verify'] = False
            if PAN_Verification.objects.filter(user = user).exists():
                data['pan_verify'] = True
            data['name'] = user.name
            return data
        raise ValidationError(response)


class SendOTPEmailSerializer(Serializer):
    email = EmailField()

    def validate(self, data):
        user = User.objects.filter(email = data['email'])
        if not user.exists():
            raise ValidationError({'message':'User not registered'})
        user = user[0]
        if resend_otp(user):
            send_email_otp(user)
        return data


class VerifyOTPEmailSerializer(Serializer):
    email = EmailField()
    otp = IntegerField()

    def validate(self, data):
        user = User.objects.filter(email = data['email'])
        if not user.exists():
            raise ValidationError({'message':'User not registered'})
        user = user[0]
        response = validateOTP(user, data['otp'])
        if response == 'OK':
            return data
        raise ValidationError(response)


class ResetPasswordSerializer(Serializer):
    email = EmailField(write_only = True)
    otp = IntegerField(write_only = True)
    password = CharField()

    def validate(self, data):
        if not self.instance.exists():
            raise ValidationError({'message':'User not registered'})
        self.instance = self.instance[0]
        otpresponse = validateOTP(self.instance, data['otp'])
        if not otpresponse == 'OK' :
            raise ValidationError({'message' : 'unauthorised access'})
        passresponse = validatePASS(data['password'], self.instance.email)
        if not passresponse == 'OK':
            raise ValidationError(passresponse)
        validateOTP(self.instance, data['otp'], resetpass = True)
        return data

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance


class SendLINKEmailSerializer(Serializer):
    email = EmailField()
    password = CharField()

    def validate(self, data):
        if User.objects.filter(email = data['email']).exists():
            raise ValidationError({'message' : 'User with this email already exists'})
        response = validatePASS(data['password'])
        if not response == 'OK':
            raise ValidationError(response)
        email = data['email']
        tokenobject = SignUpUser.objects.filter(email = email)
        if tokenobject.exists():
            if tokenobject[0].token_generated_at + timedelta(minutes=1) > timezone.now():
                raise ValidationError({'message':'wait for a minute to send another request'})
            tokenobject[0].delete()
        send_email_token(data['password'], email)
        return data


class VerifyLINKEmailSerializer(Serializer):
    email = EmailField(required = True)
    token = UUIDField(required = True)
    onapp = BooleanField(required=True)

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
        newuser = User.objects.create_user(
            email = tempuser.email,
            name = tempuser.email.split("@")[0],
            password = tempuser.password
        )
        if validated_data['onapp'] :
            return newuser.tokens()
        return {}


class CheckVerificationSerializer(Serializer):
    is_verified = BooleanField(read_only = True, default = False)
    email = EmailField(write_only = True)
    password = CharField(write_only = True)
    access = CharField(read_only = True)
    refresh = CharField(read_only = True)

    def validate(self, data):
        object = SignUpUser.objects.filter(email = data['email'])
        if not object.exists():
            raise ValidationError({'message' : 'Invalid Email'})
        object = object[0]
        if not check_password(data['password'], object.password):
            raise ValidationError({'message' : 'Unauthorised access'})
        if object.is_verified:
            data['is_verified'] = True
            user = authenticate(email=data['email'], password=data['password'])
            data['refresh'] = user.refresh
            data['access'] = user.access
            object.delete()
        return data


class VerifyPANSerializer(ModelSerializer):
    email = EmailField()
    name = CharField(required = False, allow_null = True, default = None)
    
    class Meta:
        model = PAN_Verification
        fields = ['email', 'pan_number', 'name']
        extra_kwargs = {'pan_number': {'required': False, 'allow_null': True, 'default':None}}

    def validate(self, data):
        user = User.objects.filter(email = data['email'])
        if user.exists():
            if data['pan_number'] is None:
                return data
            if PAN_Verification.objects.filter(user = user[0]).exists():
                raise ValidationError({'message':'User already verified'})
            return data
        raise ValidationError({'message':'User not registered'})
    
    def create(self, validated_data):
        holder = User.objects.get(email = validated_data['email'])
        if validated_data['pan_number'] is not None:
            PAN_Verification(
                user = holder,
                pan_number = validated_data['pan_number']
            ).save()
        if validated_data['name'] is not None:
            holder.name = validated_data['name']
            holder.save()
        return validated_data