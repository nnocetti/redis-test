import redis
import time
import random

# Esperamos que levante REDIS
time.sleep(3)

# STREAM PRODUCER

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

itemsId = '1234567'

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

print(f'Delete stream: {r.delete("test-stream")}')

while True:
  itemType = f'item-{random.choice(itemsId)}'

  ticketId = r.xadd(name='test-stream', fields={'itemType': itemType}, id='*', maxlen=100)

  print (f'producer -> Despacho    itemType: {itemType}, ticket: {ticketId}')

  # Ahora esperamos a respuesta, va estar en una lista con key igual al tickeId obtenido!
  response = r.blpop(ticketId, 2)

  if (not response):
    # Se verifica que sea por item inválido (item-7) o no haya consumidor corriendo (item-3, item-6)
    print (f'producer -> ERROR       itemType: {itemType}, ticket: {ticketId}, response: {response}')

  else:
    print (f'producer -> Comprobante itemType: {itemType}, ticket: {response[0]}, casillero: {response[1]}')

    time.sleep(2)
