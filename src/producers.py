import redis
import time
import random

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# STREAM PRODUCER
items = 'abc'

while True:
  itemId = random.choice(items)
  id = r.xadd(name='test-stream', fields={'item': f'item-{itemId}'}, id='*')
  print (id)
  time.sleep(3)