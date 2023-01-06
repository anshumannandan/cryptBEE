import cryptocompare
import time
import queue
from threading import Thread

# allcoins = cryptocompare.get_pairs(exchange='Zecoex')

# inrcoins = []
# for coin in allcoins:
#     if coin['tsym'] == 'INR':
#         inrcoins.append(coin['fsym'])

# n_threads = len(inrcoins)
# thread_list = []

# que = queue.Queue()
# for i in range(n_threads):
#     thread = Thread(target = lambda q, args : q.put({inrcoins[i] : cryptocompare.get_price(inrcoins[i], currency='INR', full=False)}), args = (que, inrcoins[i]))
#     thread_list.append(thread)
#     thread_list[i].start()

# for thread in thread_list:
#     thread.join()

# while not que.empty():
#     result = que.get()
#     print(result)