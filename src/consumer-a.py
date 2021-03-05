import redis
import time

DEPOSIT_ID = 'A'

# Esperamos que levante REDIS
time.sleep(3)
print(f'deposit{DEPOSIT_ID} -> ARRANCAMOS')

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# STREAM CONSUMER
ticketId = r.xinfo_stream('test-stream')['last-generated-id']
print(ticketId)
casillero = 0
while True:
  response = r.xread(streams={'test-stream': ticketId}, count=1, block=0)
  stream = response[0][0]
  itemType = response[0][1][0][1]['itemType']
  ticketId = response[0][1][0][0]

  time.sleep(0.1)
  print(f'deposit{DEPOSIT_ID} -> Leo         itemType: {itemType}, ticket: {ticketId}')
  time.sleep(0.1)

  if (not r.exists(itemType)):
    print(f'deposit{DEPOSIT_ID} El itemType no existe en la base de datos.')
  else:
    deposit = r.hget(itemType, 'deposit')
    if (deposit == DEPOSIT_ID):
      if (r.xdel(stream, ticketId)):

        time.sleep(0.1)
        print(f'deposit{DEPOSIT_ID} -> Guardo      itemType: {itemType}, ticket: {ticketId}, casillero: {casillero}')

        transaction = r.pipeline()
        transaction.lpush(ticketId, f'{DEPOSIT_ID}-{casillero}').expire(ticketId, 10).execute()
        casillero += 1
