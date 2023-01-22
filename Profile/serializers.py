from rest_framework.serializers import ModelSerializer, EmailField, CharField, IntegerField
from Authentication.models import User, Two_Factor_Verification
from Authentication.utils import CustomError, normalize_email, validatePASS
from django.contrib.auth.hashers import make_password, check_password
from .models import PAN_Verification
from rest_framework import status


class VerifyPANSerializer(ModelSerializer):
    email = EmailField()
    name = CharField(required = False, allow_null = True, default = None)
    
    class Meta:
        model = PAN_Verification
        fields = ['email', 'pan_number', 'name']
        extra_kwargs = {'pan_number': {'required': False, 'allow_null': True, 'default':None}}

    def validate(self, data):
        data['email'] = normalize_email(data['email'])
        user = User.objects.filter(email = data['email'])
        if user.exists():
            if data['pan_number'] is None:
                return data
            if PAN_Verification.objects.filter(user = user[0]).exists():
                raise CustomError('User already verified')
            return data
        raise CustomError('User not registered')
    
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


class ChangePasswordSerializer(ModelSerializer):
    newpassword = CharField(max_length=128, write_only = True, required = True)

    class Meta:
        model = User
        fields = ['password', 'newpassword']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def validate(self, data):
        if not check_password(data['password'], self.instance.password):
            raise CustomError("Incorrect previous password", code=status.HTTP_406_NOT_ACCEPTABLE)

        if check_password(data['newpassword'], self.instance.password):
            raise CustomError("Password same as previous password", code=status.HTTP_406_NOT_ACCEPTABLE)

        passresponse = validatePASS(data['newpassword'])
        if not passresponse == 'OK':
            raise CustomError(passresponse)

        return data

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['newpassword'])
        instance.save()
        return validated_data

    def to_representation(self, instance):
        return {'message':['Password changed successfully']}


# class EnableTwoFactorSerializer(Serializer):
#     otp = IntegerField(default = None, write_only=True)

#     class Meta:
#         model = Two_Factor_Verification
#         fields = ['phone_number', 'otp']
#         extra_kwargs = {'phone_number': {'default': None, 'write_only': True}}

    # def validate(self, data):
    #     user = self.context['request'].user

    #     try:
    #         obj = user.twofactor
    #         data['create new'] = False
    #         data['obj'] = obj
    #     except:
    #         data['create new'] = True
    #         print(data, self.model) 

    #         if data['phone_number'] is None:
    #             raise CustomError("phone_number is required")
    #         return data

    #     if obj.verified:
    #         return data

    #     if data['otp'] is None or data['phone_number'] is None:
    #         raise CustomError("phone_number and otp are required")


    #     return data

    # def create(self, validated_data):
    #     if validated_data['create new']:
    #         obj = self.model.objects.create(
    #             user = self.context['request'].user,
    #             phone_number = validated_data['phone_number']
    #         )
    #         send_two_factor_otp(obj)

    #     obj = validated_data['obj']
    #     obj.enabled = True
    #     obj.verified = True
    #     obj.save()
    #     return validated_data


class DisableTwoFactorSerializer(ModelSerializer):
    class Meta:
        model = Two_Factor_Verification
        fields = ['enabled']
 
    def validate(self, instance):
        user = self.context['request'].user
        try:
            user.twofactor
        except:
            raise CustomError('Two Factor Verification not enabled for this account')
        return {}

    def update(self, instance, validated_data):
        instance.enabled = False
        return super().update(instance, validated_data)


class ProfilePictureSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_picture']
        extra_kwargs = {'profile_picture': {'required': True}}


class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'profile_picture']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['two_factor_verification'] = False
        try:
            obj = instance.twofactor
            if obj.verified:
                if obj.enabled:
                    data['two_factor_verification'] = True
                data['phone_number'] = obj.phone_number
        except:
            pass

        try:
            obj = instance.pan_details
            data['pan_verification'] = True
            data['pan_number'] = obj.pan_number
            data['walltet'] = instance.wallet.amount
        except:
            data['pan_verification'] = False

        return data