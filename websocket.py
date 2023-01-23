import websockets
import asyncio
import os
import django
import json
from asgiref.sync import sync_to_async
from django.conf import settings
import jwt

import logging
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptBEE.settings')
django.setup()

from Authentication.models import User
from Investments.models import Coin
from django_celery_beat.models import PeriodicTask, IntervalSchedule


@sync_to_async
def AddToCeleryBeat():
    task = PeriodicTask.objects.filter(name = 'update_coins_data')
    if not task.exists():
        schedule, created = IntervalSchedule.objects.get_or_create(every = 10, period = IntervalSchedule.SECONDS)
        task = PeriodicTask.objects.create(interval = schedule, name = 'update_coins_data', task = 'Investments.tasks.update_coins')


@sync_to_async
def RemoveFromCeleryBeat():
    task = PeriodicTask.objects.filter(name = 'update_coins_data')
    if task.exists():
        task.delete()


@sync_to_async
def holdings_data(user):
    holdings = []
    try:
        for holding in user.my_holdings.MyHoldings:
            coin = Coin.objects.get(Name = holding[0])
            holdings.append({"Name" : coin.Name, "FullName": coin.FullName, "ImageURL" : coin.Image, "Coins" : holding[1]})
    except:
        pass
    return holdings


@sync_to_async
def particular_holdings_data(user, reqd_coin):
    holdings = []
    try:
        for holding in user.my_holdings.MyHoldings:
            coin = Coin.objects.get(Name = holding[0])
            if reqd_coin == coin:
                holdings.append({"Name" : coin.Name, "FullName": coin.FullName, "ImageURL" : coin.Image, "Coins" : holding[1]})
                break
    except:
        pass
    return holdings


async def socket(websocket, user):
    try:
        while True:
            coins = Coin.objects.all()
            data = []
            async for coin in coins:
                data.append({'Name': coin.Name, 'FullName' : coin.FullName, 'Price': coin.Price, 'ChangePct': coin.ChangePct, 'ImageURL': coin.Image})
            holdings = await holdings_data(user)
            await websocket.send(json.dumps({'data': data, 'holdings' : holdings}))
            await asyncio.sleep(10)
    except websockets.ConnectionClosedOK:
        return


async def single_socket(websocket, user, req):
    try:
        while True:
            coin = await get_coin(req)
            data = {'Name': coin.Name, 'FullName' : coin.FullName, 'Price': coin.Price, 'ChangePct': coin.ChangePct, 'ImageURL': coin.Image}
            holdings = await particular_holdings_data(user, coin)
            await websocket.send(json.dumps({'data': data, 'holdings' : holdings}))
            await asyncio.sleep(10)
    except websockets.ConnectionClosedOK:
        return


@sync_to_async
def get_coin(name):
    try:
        return Coin.objects.get(Name = name)
    except:
        return False


async def handler(websocket, user):
    global connected
    connected.add(websocket)
    if len(connected) == 1:
        await AddToCeleryBeat()
    await websocket.send('authorised, enter ALL or name of the coin')
    req = await websocket.recv()
    if req == 'ALL':
        await socket(websocket, user)
    else:
        coin = await get_coin(req)
        if not coin:
            await websocket.send('invalid request')
        await single_socket(websocket, user, req)
    connected.remove(websocket)
    if len(connected) == 0:
        await RemoveFromCeleryBeat()


@sync_to_async
def get_user(tokenset):
    return User.objects.get(id = tokenset['user_id'])


async def authorise(websocket):
    await websocket.send('connection established, send token to recieve data')    
    token = await websocket.recv()
    try: 
        tokenset = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except:
        await websocket.send('invalid token')
        return
    user = await get_user(tokenset)
    await handler(websocket, user)


async def main():
    async with websockets.serve(authorise, port = 8001):
        await asyncio.Future()


connected = set()
asyncio.run(main())