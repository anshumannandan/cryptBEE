from django.db.models.base import Model
from django.db.models.fields import FloatField, CharField, URLField, TextField, DateTimeField
from django.db.models.fields.related import OneToOneField
from django.db.models import CASCADE
from django_better_admin_arrayfield.models.fields import ArrayField
import datetime
from Authentication.models import User


class Coin(Model):
    Name = CharField(max_length=10, unique=True, null=True, blank=True)
    FullName = CharField(max_length=100, unique=True, null=True, blank=True)
    Price = FloatField(null=True, blank=True)
    ChangePct = FloatField(null=True, blank=True)
    Image = URLField(null=True, blank=True)
    Description = TextField(null=True, blank=True)

    def __str__(self):
        return '%s : %s' % (self.Name, self.Price)

    class Meta:
        ordering = ['Name']


class MyHoldings(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='my_holdings')
    MyHoldings = ArrayField(ArrayField(CharField(max_length=20, blank=True), size = 2), blank=True)


class TransactionHistory(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='transactions')
    transactions = ArrayField(CharField(max_length=255, blank=True), null = True, blank = True)


class MyWatchlist(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='watchlist')
    watchlist = ArrayField(CharField(max_length=10, blank=True), null = True, blank = True)


class News(Model):
    headline = CharField(max_length=255)
    news = URLField()
    image = URLField()


class BuyLock(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='buy')
    coin = CharField(max_length=10)
    price = FloatField()
    time = DateTimeField(default=datetime.datetime(1000, 1, 1, 0, 0, 0))


class SellLock(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='sell')
    coin = CharField(max_length=10)
    price = FloatField()
    time = DateTimeField(default=datetime.datetime(1000, 1, 1, 0, 0, 0))