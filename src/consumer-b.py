import redis

print('arrancamos')

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)


# STREAM CONSUMER (blocking, one by one, all in the stream, si queremos solo el ultimo lanzado utilizamos como id '$')
id = 0
while True:
  response = r.xread(streams={'test-stream': id}, count=1, block=0)
  print(response)
  stream = response[0][0]
  id = response[0][1][0][0]
  item = response[0][1][0][1]['item']
  print(f'stream {stream}')
  print(f'id {id}')
  print(f'item {item}')
