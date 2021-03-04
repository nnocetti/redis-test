import redis
import time
import random

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# PUB/SUB PATTERN PRODUCER
while True:
  r.publish('test', time.ctime(time.time()))
  time.sleep(3)
