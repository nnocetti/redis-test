# redis-test
Pruebas de diferentes patrones para la comunicación entre programas utilizando la base de datos en memoria Redis y el lenguaje de programación Python con la librería redis-py.

Este es un ejemplo más complejo, supongamos que tengo ítems de distinto tipo, (1, 2, 3, 4, 5, 6, 7), y un grupo de depósitos (a, b, c), los ítems en función de su tipo se deben guardar en un depósito especifico.  
Es importante informar en que depósito y casillero del mismo se guardó un ítem. Así los ítems son despachados por los productores y guardados en los distintos depósitos por los consumidores, además el proceso que despacho el ítem (productor) debe ser informado no solo del depósito donde fue guardado, sino también del casillero asignado dentro del depósito.  
Se debe tener en cuenta que la relación entre los ítems y los depósitos puede cambiar.  

La idea atrás del ejemplo es que yo tengo distintos tipos de task, con información asociada, y en función de esa información debo asignarla a un determinado worker, pero solo con la información asociada a la tarea no puedo saber a qué worker asignarla, necesito consultar la BD Redis con información suplementaria para poder asignar la task.  
