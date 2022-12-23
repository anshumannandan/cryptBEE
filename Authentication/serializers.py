from rest_framework.serializers import Serializer, CharField, BooleanField
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Two_Factor_Verification, PAN_Verification


class LoginSerializer(Serializer):
    email = CharField(write_only=True)
    password = CharField(write_only=True)
    two_factor = BooleanField(read_only=True)
    refresh = CharField(read_only=True)
    access = CharField(read_only=True)
    pan_verify = BooleanField(read_only=True)

    def validate(self,data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise ValidationError('Invalid Credentials')
        try:
            Two_Factor_Verification.objects.get(user = user)
            data['two_factor'] = True
        except:
            data['refresh'] = user.refresh
            data['access'] = user.access
            data['two_factor'] = False
            try:
                PAN_Verification.objects.get(user = user)
                data['pan_verify'] = True
            except:
                data['pan_verify'] = False
        return data

    def create(self, validated_data):
        return validated_data