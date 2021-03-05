import redis
import time

DEPOSIT_ID = 'B'

# Esperamos que levante REDIS
time.sleep(3)
print(f'deposit{DEPOSIT_ID} -> ARRANCAMOS')

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# STREAM CONSUMER
ticketId = r.xinfo_stream('test-stream')['last-generated-id']
casillero = 0

while True:
  response = r.xread(streams={'test-stream': ticketId}, count=1, block=0)
  ticketId = response[0][1][0][0]
  itemType = response[0][1][0][1]['itemType']

  deposit = r.hget(itemType, 'deposit')
  if (deposit == DEPOSIT_ID):
    if (r.xdel('test-stream', ticketId)):

      transaction = r.pipeline()
      transaction.lpush(ticketId, f'{DEPOSIT_ID}-{casillero}').expire(ticketId, 10).execute()
      casillero += 1
