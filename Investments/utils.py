import cryptocompare
from .models import Coin
from django.conf import settings
from Authentication.models import User
import jwt
from Authentication.utils import CustomError
from rest_framework import status


def update_coin_database():
    coins = []
    for coin in cryptocompare.get_pairs(exchange='Zecoex'):
        if coin['tsym'] == 'INR':
            coins.append(coin['fsym'])
    dbcoins = Coin.objects.all()
    dbcoinsmap = {}
    newcoins = []
    for coin in dbcoins:
        dbcoinsmap[coin.Name] = True
    for coin in coins:
        try:
            dbcoinsmap[coin]
        except:
            newcoins.append(coin)
    if len(newcoins) != 0:
        fetchedcoins = cryptocompare.get_coin_list(format=False)
        for coin in newcoins:
            try:
                curcoin = fetchedcoins[coin]
            except:
                continue
            Coin.objects.create(
                Name=coin,
                FullName=curcoin['CoinName'],
                Image='cryptocompare.com'+curcoin['ImageUrl'],
                Description=curcoin['Description'],
            )


def update_transaction_history():
    pass


def update_my_holdings():
    pass