# redis-test
Pruebas de diferentes patrones para la comunicación entre programas utilizando la base de datos en memoria Redis y el lenguaje de programación Python con la librería redis-py.

* Prueba simple del data type PUB/SUB. https://github.com/nnocetti/redis-test/tree/SimplePub/Sub

* Prueba simple del data type Stream. https://github.com/nnocetti/redis-test/tree/SimpleStream

* Prueba del data type Stream utilizado como colas con respuesta sincrónica. https://github.com/nnocetti/redis-test/tree/StreamAsQueue

* Prueba de carga del modelo StreamAsQueue. https://github.com/nnocetti/redis-test/tree/StreamAsQueueLoadTest

La rama main contiene un paquete con la clase SyncStream que intenta representar una abstracción de un stream sincrónico.

Posee únicamente dos métodos pop and push, ambos bloqueantes.

### Productores (los que hacen push)

* Varios pueden compartir una instancia de la clase.

### Consumidores (los que hacen pop)

* Cada consumidor debe utilizar su propia instancia, sino se corre el riesgo de perder mensajes.

* Procesan mensajes insertados en el stream posteriores al momento que se instancia la clase.

Se puede ser productor y consumidor.

Importante:  
En función del uso del stream se debe ajustar la propiedad stream_maxlen, la idea de la misma es evitar que elementos insertados en el stream queden colgados para siempre. Lamentablemente Redis no dispone de un timeout para elementos del stream pero si se puede definir una máxima cantidad de elementos, de modo que al insertar nuevos, si se supera la máxima cantidad los elementos más antiguos se eliminan.  
El valor por defecto de maxlen es 1000, puede ser un valor elevado cuando la cantidad de inserciones por segundo es baja.  
En este ejemplo se presentan 750 productores, haciendo una solicitud por segundo y 9 consumidores que responden inmediatamente; el tamaño del stream ronda los 600-650 elementos. Por lo que en un entorno en el que se supere las 500 inserciones por segundo sería recomendable aumentar el stream_maxlen.