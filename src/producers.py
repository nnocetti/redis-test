import redis
import time
import random
import threading

# Este es un ejemplo más complejo, supongamos que tengo items de distinto tipo, (1, 2, 3, 4, 5, 6, 7),
# y un grupo de depositos (a, b, c), los items en función de su tipo se deben guardar en un depósito especifico.
# Es importante informar en que depósito y casillero del mismo se guardo un ítem.
# Así los items son despachados por los productores y guardados en los distintos depositos por los consumidores,
# además el proceso que despacho el ítem (productor) debe ser informado no solo del depósito donde fue guardado,
# sino del casillero asignado dentro del depósito.
# Se debe tener en cuenta que la relación entre los items y los depositos puede cambiar.

# La idea atras del ejemplo es que yo tengo distintos tipos de task, con información
# asociada, y en función de esa información debo asignarla a un determinado worker, pero solo con la información
# asociada a la tarea no puedo saber a que worker asignarla, necesito consultar la BD Redis con información
# suplementaria para poder asignar la task.

# Esperamos que levante REDIS y los consumidores
time.sleep(4)

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

def createProducer(producerId):
  while True:
    itemType = f'item-{random.choice(itemsId)}'

    ticketId = r.xadd(name='test-stream', fields={'itemType': itemType}, id='*', maxlen=1000000)

    # Ahora esperamos a respuesta, va estar en una lista con key igual al tickeId obtenido!
    response = r.blpop(ticketId, 1)

    if (not response and itemType not in ('item-3', 'item-6', 'item-7')):
      print (f'producer{producerId} -> ERROR      itemType: {itemType}, ticket: {ticketId}')

    time.sleep(0.5)

producers = list()
for producerId in range(10000):
  producer = threading.Thread(target=createProducer, args=(producerId, ))
  producer.start()
