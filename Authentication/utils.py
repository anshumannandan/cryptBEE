from twilio.rest import Client
from django.conf import settings
import random
from . models import Two_Factor_OTP, Email_OTP
from django.utils import timezone


def send_two_factor_otp(mobile):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    otp = random.randint(1000, 9999)
    phone_number = '+91' + str(mobile.phone_number)
    client.messages.create(
        body=f"Use the following OTP for CryptBee Two Factor Authentication.\nOTP : {otp}, valid for only 2 minutes",
        from_=settings.TWILIO_DEFAULT_CALLERID,
        to=phone_number
    )
    Two_Factor_OTP(
        phone_number = mobile,
        otp = otp,
        created_time = timezone.now()
    ).save()