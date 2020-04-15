# Tarea 1 Saúl Badillo Hernández.
---------------

* Problema: Resolví el problema número 3, El elevador.  
* Lenguaje: C  
	* Para correr el programa puede usar el siguiente comando desde una terminal de linux `gcc -std=c99 elevador.c -lpthread && ./a.out`  
* Estoy utilizando una condición de variable para limitar quienes pueden entrar o salir del elevador por el piso en el que están y un semaforo para limitar la cantidad de alumnos que entran al elevador  
* Sin refinamiento por el momento  
* El elevador sólo sube y se queda así, estoy pensando en usar 2 mutex más para tener dirección (sube y baja), así como el piso al que va dirigido (Para que no haga todo el recorrido si no es necesario hacerlo)   
