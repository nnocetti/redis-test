import redis
import time
import random
import threading
import string

from sstream.redis_sync_stream import SyncStream

DEPOSIT_STREAM = 'deposit-stream'

# Esperamos que levante REDIS y los consumidores
time.sleep(6)

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

itemsId = '123456'

# STREAM PRODUCER
def cproducer(producerId):
  sstream = SyncStream(r, DEPOSIT_STREAM)

  while True:
    itemType = f'item-{random.choice(itemsId)}'

    response = sstream.push(itemType, ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)))

    if (not response):
      if (itemType not in ('item-3', 'item-6', 'item-7')):
        print (f'producer{producerId} -> ERROR      itemType: {itemType}')
    else:
      #print (f'producer{producerId} -> {response}')
      pass

    time.sleep(1)

producers = list()
for producerId in range(750):
  producer = threading.Thread(target=cproducer, args=(producerId, ))
  producer.start()
  time.sleep(0.01)
