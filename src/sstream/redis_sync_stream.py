from typing import Callable
from redis import Redis

class SyncStream:
  # Class variables
  db_task_type_label: str = 'task'
  db_task_data_label: str = 'data'
  db_worker_type_label: str = 'worker'

  def __init__(self, db: Redis, name: str, worker_type: str = None):
    # Instance variables
    self.stream_maxlen: int = 1000
    self.push_timeout: int = 30
    self.response_ttl: int = 10

    self.db = db
    self.stream_name = name
    self.worker_type = worker_type

    self.current_id = 0
    # Si el stream existe, se actualiza el current_id al último ingresado en el stream.
    if (self.db.exists(self.stream_name)):
      self.current_id = self.db.xinfo_stream(self.stream_name)['last-generated-id']

  def push(self, task_type: str, data: str, timeout: int = None) -> str:
    if (not timeout):
      timeout = self.push_timeout

    # Agregamos una tarea al stream stream_name, de tipo task_type con información data.
    # El parámetro '*' indica a redis asigne un id automáticamente.
    # Con el parámetro maxlen truncamos la capacidad del stream a un máximo para limpiar tareas colgadas en el stream.
    id = self.db.xadd(self.stream_name, {self.db_task_type_label: task_type, self.db_task_data_label: data}, '*', self.stream_maxlen)

    # Ahora esperamos a que un worker tome la tarea y nos responda.
    # La respuesta se guarda en una lista con key igual al id obtenido.
    response = self.db.blpop(id, timeout)
    if (response):
      response = response[1]

    return response

  def pop(self, callback: Callable[[str, str, str], str], ttl: int = None) -> None:
    if (not self.worker_type):
      raise('Se debe definir tipo de worker a traves de la propiedad "worker_type"')

    if (not ttl):
      ttl = self.response_ttl

    while True:
      # Leemos nuevos mensajes en el stream a partir de "current_id".
      # se actualiza current_id a medida que se lee.
      message = self.db.xread(streams={self.stream_name: self.current_id}, count=1, block=0)
      self.current_id = message[0][1][0][0]
      task_type = message[0][1][0][1][self.db_task_type_label]
      task_data = message[0][1][0][1][self.db_task_data_label]

      if (self.worker_type == self.db.hget(task_type, self.db_worker_type_label)):
        if (self.db.xdel(self.stream_name, self.current_id)):

          # Si la tarea tiene como destino un consumidor del tipo indicado y se pudo "tomar" antes que otro worker, se llama a la función callback para procesarla.
          consumer_response = callback(task_data, task_type, self.current_id)

          # Se asigna un ttl al registro para que si por alguna razón el productor no sustrae la información, la misma no quede como basura en la base de datos.
          # Se unifican las dos operaciones en una transacción.
          txn = self.db.pipeline()
          txn.lpush(self.current_id, consumer_response).expire(self.current_id, ttl).execute()

          # Luego de procesar una task, termina el bucle.
          break
