import websockets
import asyncio
import os
import django
import json
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptBEE.settings')
django.setup()

from Investments.models import Coin
from django_celery_beat.models import PeriodicTask, IntervalSchedule


@sync_to_async
def AddToCeleryBeat():
    task = PeriodicTask.objects.filter(name = 'update_coins_data')
    if not task.exists():
        schedule, created = IntervalSchedule.objects.get_or_create(every = 20, period = IntervalSchedule.SECONDS)
        task = PeriodicTask.objects.create(interval = schedule, name = 'update_coins_data', task = 'Investments.tasks.update_coins')


@sync_to_async
def RemoveFromCeleryBeat():
    task = PeriodicTask.objects.filter(name = 'update_coins_data')
    if task.exists():
        task.delete()


async def echo(websocket):
    global connections
    print('new connection added,', connections+1, 'clients connected')
    if connections == 0 : 
        await AddToCeleryBeat()
    try:
        connections += 1
        while True:
            coins = Coin.objects.all()
            data = []
            async for coin in coins:
                data.append({'Name': coin.Name, 'Price': coin.Price, 'ChangePct': coin.ChangePct})
            await websocket.send(json.dumps({'data': data}))
            await asyncio.sleep(20)
    except:
        connections -= 1
        print(connections, 'clients connected')
        if connections == 0:
            await RemoveFromCeleryBeat()
        return


async def main():
    async with websockets.serve(echo, port = 8001):
        await asyncio.Future()


print('server started...')
connections = 0
asyncio.run(main())