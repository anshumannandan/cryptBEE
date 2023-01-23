import cryptocompare
from Authentication.utils import CustomError
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


def update_my_holdings(obj, coinname, number_of_coins):
    found = False
    updated_holdings = []
    for i in obj.MyHoldings:
        if i[0] == coinname:
            found = True
            if round( float(i[1]) + number_of_coins, 8) == 0:
                continue
            updated_holdings.append([i[0], round( float(i[1]) + number_of_coins, 8)])
        else:
            updated_holdings.append(i)
    if not found : 
        updated_holdings.append([coinname, number_of_coins])
    obj.MyHoldings = updated_holdings
    obj.save()