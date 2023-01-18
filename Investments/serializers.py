from .models import *
from rest_framework.serializers import Serializer, CharField, FloatField
from .utils import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
import time

datee = lambda : date.today().strftime("%B %d; %Y")
timee = lambda : time.strftime("%H:%M:%S")


class BuyCoinSerializer(Serializer):
    coin_name = CharField(write_only = True)
    buy_amount = FloatField(write_only = True)
    price = FloatField(write_only = True)

    def validate(self, data):
        user = self.context['request'].user

        try: 
            user.pan_details
        except ObjectDoesNotExist:
            raise CustomError("Verify yourself with PAN to trade", code=status.HTTP_406_NOT_ACCEPTABLE)

        coin = Coin.objects.filter(Name = data['coin_name'])
        if not coin.exists():
            raise CustomError("Coin not available to trade", code=status.HTTP_404_NOT_FOUND)

        wallet = user.wallet
        if wallet.amount < data['buy_amount']:
            raise CustomError("Insufficient wallet balance", code=status.HTTP_403_FORBIDDEN)

        if data['buy_amount'] < 1:
            raise CustomError("Invalid amount, you need to spend atleast INR 1")

        if not ( data['price'] == coin[0].Price or data['price'] == coin[0].lastPrice ):
            raise CustomError("Invalid Price", code=status.HTTP_403_FORBIDDEN)

        data['coin'] = coin[0]
        data['user'] = user
        data['wallet'] = wallet
        return data

    def create(self, validated_data):
        price = validated_data['price']
        coinname = validated_data['coin_name']
        amount = validated_data['buy_amount']

        validated_data['wallet'].amount -= amount
        validated_data['wallet'].save()

        number_of_coins = amount / price

        obj = validated_data['user'].transactions
        obj.transactions.append(
            f' Bought {number_of_coins} {coinname} on {datee()} at {timee()} at price {price}')
        obj.save()

        obj = validated_data['user'].my_holdings
        update_my_holdings(obj, coinname, number_of_coins)

        return {'coins' : number_of_coins}