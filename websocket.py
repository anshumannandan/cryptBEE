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


async def socket(websocket):
    try:
        coins = Coin.objects.all()
        while True:
            data = []
            async for coin in coins:
                data.append({'Name': coin.Name, 'FullName' : coin.FullName, 'Price': coin.Price, 'ChangePct': coin.ChangePct, 'ImageURL': coin.Image})
            await websocket.send(json.dumps({'data': data}))
            await asyncio.sleep(10)
    except websockets.ConnectionClosedOK:
        return


async def handler(websocket):
    global connected
    connected.add(websocket)
    if len(connected) == 1:
        await AddToCeleryBeat()
    await socket(websocket)
    connected.remove(websocket)
    if len(connected) == 0:
        await RemoveFromCeleryBeat()
    await websocket.send('authorised, enter ALL or name of the coin')
    # req = await websocket.recv()
    # if req == 'ALL':
    #     await socket(websocket)
    # else:
    #     return


async def authorise(websocket):
    await websocket.send('connection established, send token to recieve data')    
    token = await websocket.recv()
    try: 
        jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        await handler(websocket)
    except:
        await websocket.send('invalid token')


async def main():
    async with websockets.serve(authorise, port = 8001):
        await asyncio.Future()


connected = set()
asyncio.run(main())