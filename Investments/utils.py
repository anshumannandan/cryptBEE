import cryptocompare
from .models import Coin


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