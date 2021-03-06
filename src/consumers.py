import redis
import time
import threading

from sstream.redis_sync_stream import SyncStream

DEPOSIT_STREAM = 'deposit-stream'

# Esperamos que levante REDIS
time.sleep(2)
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# Cargamos la BD
item1 = {'deposit': 'A', 'comment': 'other data 1'}
item2 = {'deposit': 'B', 'comment': 'other data 2'}
item3 = {'deposit': 'C', 'comment': 'other data 3'}
item4 = {'deposit': 'A', 'comment': 'other data 4'}
item5 = {'deposit': 'B', 'comment': 'other data 5'}
item6 = {'deposit': 'C', 'comment': 'other data 6'}

r.hmset('item-1', item1)
r.hmset('item-2', item2)
r.hmset('item-3', item3)
r.hmset('item-4', item4)
r.hmset('item-5', item5)
r.hmset('item-6', item6)


print(f'Delete stream: {r.delete(DEPOSIT_STREAM)}')


# STREAM CONSUMER
def cconsumer(depositType, depositId):
  locker = 0
  SyncStream.db_worker_type_label = 'deposit'
  sstream = SyncStream(r, DEPOSIT_STREAM, depositType)

  # Funcion a ejecutar al obtener una task
  def storeItem(data, itemId, streamId) -> str:
    #print(f'deposit{depositId} -> {itemId}: {data}, locker: {locker}') 
    return f'{depositId}:{locker}:{itemId}:{data}'

  print(f'deposit{depositId} -> ARRANCAMOS')

  while True:
    sstream.pop(storeItem)
    locker += 1

consumers = list()
for consumerType in ('A', 'B', 'C'):
  for consumerNum in range(3):
    consumerId = f'{consumerType}-{consumerNum}'
    consumer = threading.Thread(target=cconsumer, args=(consumerType, consumerId))
    consumer.start()