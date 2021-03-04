import redis

print('arrancamos')

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# PUB/SUB PATTERN CONSUMER 
p = r.pubsub()
p.subscribe('test')

for message in p.listen():
  print(message)
