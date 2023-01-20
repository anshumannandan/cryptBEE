import websockets
import asyncio
import os
import django
import json
from asgiref.sync import sync_to_async
from django.conf import settings
import jwt

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


@sync_to_async
def is_valid(token):
    try: 
        jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except:
        return False
    return True


async def socket(websocket):
    await websocket.send('connection established, send token to recieve data')
    
    token = await websocket.recv()
    if not await is_valid(token):
        await websocket.send('invalid token')
        return 

    global connections
    connections += 1
    print('new connection added,', connections, 'clients connected')

    if connections == 1:
        await AddToCeleryBeat()

    await asyncio.sleep(1)
    
    try:
        while True:
            coins = Coin.objects.all()
            data = []
            async for coin in coins:
                data.append({'Name': coin.Name, 'FullName' : coin.FullName, 'Price': coin.Price, 'ChangePct': coin.ChangePct, 'ImageURL': coin.Image})
            await websocket.send(json.dumps({'data': data}))
            await asyncio.sleep(1)
    except:
        connections -= 1
        print('client disconnected,', connections, 'clients connected')
    
    if connections == 0:
        await RemoveFromCeleryBeat()


async def main():
    async with websockets.serve(socket, port = 8001):
        print('server started...')
        await asyncio.Future()

connections = 0
asyncio.run(main())