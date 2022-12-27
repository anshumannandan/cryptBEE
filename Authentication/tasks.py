from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from twilio.rest import Client
from django.conf import settings


@shared_task(bind = True)
def send_email_through_celery(self, subject, html_content, recepient):
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST,
            [recepient]
            )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return subject + ' EMAIL SENT'


@shared_task(bind = True)
def send_sms_through_celery(self, otp, recepient):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f"Use the following OTP for CryptBee Two Factor Authentication.\nOTP : {otp}, valid for only 2 minutes",
        from_=settings.TWILIO_DEFAULT_CALLERID,
        to=f"+91{recepient}"
    )
    return 'SMS SENT'