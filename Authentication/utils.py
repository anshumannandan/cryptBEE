from twilio.rest import Client
from django.conf import settings
import random
from . models import Two_Factor_OTP, Email_OTP
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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


def validateOTP(user, otp, twofactor=False):
    if twofactor:
        try:
            otpobject = user.twofactor.twofactorotp
            validity = 2
        except:
            return {'message' : 'Please resend OTP'}
    else:
        try:
            otpobject = user.emailotp
            validity = 5
        except:
            return {'message' : 'Please resend OTP'}
    if otpobject.created_time + timedelta(minutes=validity) < timezone.now():
        otpobject.delete()
        return {'message' : 'OTP timed out'}
    if otpobject.otp == int(otp):
        otpobject.delete()
        return 'OK'
    return  {'message' : 'OTP Invalid'}


def send_email_otp(user):
    otp = random.randint(1000, 9999)
    mailaddress = user.email
    name = user.name
    html_content = render_to_string("sendotp.html", {"otp": otp,"name": name})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
                "CryptBee Password Reset",
                text_content,
                settings.EMAIL_HOST,
                [mailaddress]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    Email_OTP(
        user = user,
        otp = otp,
        created_time = timezone.now()
    ).save()


def resend_otp(user, twofactor = False):
    if twofactor:
        try:
            otpobject = user.twofactor.twofactorotp
        except:
            return True
    else:
        try:
            otpobject = user.emailotp
        except:
            return True
    if otpobject.created_time + timedelta(minutes=1) > timezone.now():
        return False
    otpobject.delete()
    return True