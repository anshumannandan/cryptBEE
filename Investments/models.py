from django.db.models.base import Model
from django.db.models.fields import FloatField, CharField, URLField, TextField
from django.db.models.fields.related import OneToOneField
from django.db.models import CASCADE
from Authentication.models import User
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
import string    
import random


class Coin(Model):
    Name = CharField(max_length=10, unique=True)
    FullName = CharField(max_length=100, unique=True)
    Price = FloatField(null=True, blank=True)
    lastPrice = FloatField(null=True, blank=True)
    ChangePct = FloatField(null=True, blank=True)
    Image = URLField()
    Description = TextField()

    def __str__(self):
        return '%s : %s' % (self.Name, self.Price)

    class Meta:
        ordering = ['Name']


class PAN_Verification(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='pan_details')
    pan_number = CharField(unique=True, max_length=10,
                           validators=[RegexValidator(regex='[A-Z]{5}[0-9]{4}[A-Z]{1}', message='Invalid PAN',),])

@receiver(post_save, sender=PAN_Verification)
def create_referal_code(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user = instance.user)
        MyHoldings.objects.create(user =instance. user,  MyHoldings = [])
        TransactionHistory.objects.create(user = instance.user)

class Wallet(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='wallet')
    amount = FloatField(default=1000)
    referal = CharField(max_length=6, null=True, blank=True)

@receiver(post_save, sender=Wallet)
def make_referal_code(sender, instance, created, **kwargs):
    if created:
        id = str(instance.user.id)
        instance.referal = ''.join(random.choices(string.ascii_uppercase, k = 6 - len(id))) + id
        instance.save()


class MyHoldings(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='my_holdings')
    MyHoldings = ArrayField(ArrayField(CharField(max_length=20, blank=True), size = 2), blank=True)


class TransactionHistory(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='transactions')
    transactions = ArrayField(CharField(max_length=255, blank=True), null = True, blank = True)