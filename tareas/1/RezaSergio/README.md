#Tarea 1: Ejercicio de sincronización Alumnos y Asesor
Reza Chavarria Sergio Gabriel

#Resolución
Se realizó la resolución del problema de sincronización de Alumnos y Asesor.


Se utilizó el lenguaje de programación Python versión
	
	Python 3.6.9

Uso del comando:
	
	python3 Tarea1RezaSergio.py


#Forma de resolución
La forma en la que le di una resolución al problema fue a través del uso de Candados para la Exclusión mutua. Esto se utilizó para que el alumno que tenga el candado sea el único en preguntar al profesor sin que se saturé la consulta.
Se dio uso de los multiplex. Esto se utilizó para la cantidad de hilos que el profesor puede atender.



Para variar la cantidad de alumnos, preguntas a realizar y asientos disponibles modificar.

	10-		lugar=Semaphore(5)
	35-		for i in range (10):
	36- 	preguntas=randrange(1,4)

Nota: como comentarios deje las formas en las que al inicio planteé la resolución