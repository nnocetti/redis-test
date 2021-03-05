# redis-test
Prubeas de diferentes patrones para la comunicación entre programas utilizando la base de datos en memoria Redis y el lenguaje de programación Python con la libreria redis-py.

Este es un ejemplo más complejo, supongamos que tengo items de distinto tipo, (1, 2, 3, 4, 5, 6, 7), y un grupo de depositos (a, b, c), los items en función de su tipo se deben guardar en un depósito especifico.  
Es importante informar en que depósito y casillero del mismo se guardo un ítem. Así los items son despachados por los productores y guardados en los distintos depositos por los consumidores, además el proceso que despacho el ítem (productor) debe ser informado no solo del depósito donde fue guardado, sino tambien del casillero asignado dentro del depósito.  
Se debe tener en cuenta que la relación entre los items y los depositos puede cambiar.  

La idea atras del ejemplo es que yo tengo distintos tipos de task, con información asociada, y en función de esa información debo asignarla a un determinado worker, pero solo con la información asociada a la tarea no puedo saber a que worker asignarla, necesito consultar la BD Redis con información suplementaria para poder asignar la task.  