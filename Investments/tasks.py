from celery import shared_task
import cryptocompare
import time
import queue
from threading import Thread
from .models import Coin


@shared_task(bind=True)
def update_coins(self):
    coins = Coin.objects.all()
    threadlist = []
    que = queue.Queue()
    for coin in coins:
        thread = Thread(target=lambda q, args: q.put({coin.Name: cryptocompare.get_price(
            coin.Name, currency='INR', full=True)}), args=(que, coin.Name))
        threadlist.append(thread)
        threadlist[-1].start()
        if len(threadlist) == 50:
            time.sleep(1)
    for thread in threadlist:
        thread.join()
    data = {}
    while not que.empty():
        result = que.get()
        data.update(result)
    for coin in coins:
        coindata = data[coin.Name]['RAW'][coin.Name]['INR']
        coin.Price = coindata['PRICE']
        coin.ChangePct = coindata['CHANGEPCTHOUR']
        coin.save()
    return 'COINS UPDATED'
