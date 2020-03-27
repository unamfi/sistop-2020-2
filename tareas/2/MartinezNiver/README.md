## Ejercicios de algoritmos de planificación

# Algoritmos resultos:
- FCFS. Cuenta con su propio algoritmo que va calculando la información deseada.
- RR1. En este caso, se partió de un algortimo que se pudiera ampliar al variar q.
- RR4. Se realizó a parti de RR4, con la variación del parámetro q.

# Métodos utilizados:
- init_arrives() : Genera los tiempos de llegada de cada proceso de
	de manera aleatoria para un número n de procesos.

- generator_time() : Genera los tiempos que requiere cada proceso para
	terminar su ejecución de de manera aleatoria para 
	un número n de procesos.

- time_process() : Genera un diccionario que contiene como llaves el 
	nombre del proceso y como valores una lista con
	los tiempos de llegada y de ejecución.

- divide_list() : Nos ayuda a realizar la división elemento por
	elemento de dos listas.

- average() : Reliza el promedio (media aritmética) de todos
	 los elementos de una lista.

- Además de los algoritmos implementados.

# Ejecución:

Se trabajo en gran medida, como programación estruturada, por lo que no requiere
de procedimientos extra para ser ejecutado. Esta elaborado en python3, por lo que
basta con ejecutar desde terminar de la siguiente manera:

	$ python3 <file_name>


## Notas:

# - Sobre el nombre de los procesos.
	Los nombre de cada proceso son letras mayúsculas, por conveniencia,
	si se quiere agregar más letras se debe de especificar en el main, agregando
	un elemento a la lista de nombres, en orden alfabético.
# - Sobre la representación.
	Aún no logré la modularización más adecuada para poder hacer encajar las
	piezas que me permitieran dejar lista la representación de como se va
	ejecutando cada parte de los procesos (mediante letras) en RR para q=1 y q=4.
# - Sobre los parámetros y variables.
	Hay dos variables en el main que sirven para remplazarse en los parámetros
	de los algoritmos. Uno de ellos es n, que es el número de procesos y el otro
	es m, que es el número de rondas.
# - Sobre los encabezados.
	Son estáticos ya que se pensó en 5 procesos como máximo para esta implmentación,
	así que podrían verse cortos o desfazados si se modifica m y n.


## Pruebas:

	Se incluyen imagen de las prueba de ejecución.

 ![captura_planif](images/captura_planif.png)

