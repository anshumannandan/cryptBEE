import websockets
import asyncio
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptBEE.settings')
django.setup()

from Investments.models import Coin

async def echo(websocket):
    try:
        await websocket.send('connection established')
        while True:
            coins = Coin.objects.all()
            data = {}
            async for coin in coins:
                data[coin.Name] = {'Price': coin.Price, 'ChangePct': coin.ChangePct}
            await websocket.send(json.dumps(data))
            await asyncio.sleep(20)
    except:
        return


async def main():
    async with websockets.serve(echo, "localhost", 8001):
        await asyncio.Future()
asyncio.run(main())
asyncio.run(main())