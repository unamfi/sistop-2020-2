TAREA 1: Ejercicios de sincronización
=======================================================

INTEGRANTES:
=============================

* Alfonso Murrieta Villegas
* Valdespino Mendieta Joaquín

Descripción General:
=============================
A través del patrón del APAGADOR y MUTEX es cómo se realizó el debido ejercicio de sincronización, cabe destacar que la premisa 
principal y aspecto más considerado durante todo el problema fue el que los gatos respectaran el que comieran los ratones a menos de que estos estuvieran antes comiendo a lo que directamente se comerían los o el ratón (Aquí tuvimos un poco de duda)

PROBLEMA: Gatos y ratones 
=================

Lenguaje de Programación :
* Python en su versión 3.7
* Paradigma Orientado a Objetos*

Ejecución del programa:
*  python3 gatosRatones.py

Notas:
* Para modificar el número de platos es necesario modificar la linea 19-> numDish = threading.Semaphore(NUMERO) 

ESTRATEGIA: 
=================
Como se mencionó previamente, se emplearon mutex para resguardar la seguridad de cada uno de los hilos, sin embargo, el elemento principal para evitar inanición y bloqueos mutuos fue el patrón del APAGADOR, debido sobre todo a la similitud de este ejercicio respecto al problema de lectores y escritores, además de que los procesos debían excluirse de secciones críticas, se decidió abordar este patrón como solución. 

Notas:
* Para más detalles, el código se encuentra documentado en cada una de sus clases, tanto en sus métodos como atributos.


DUDAS:
==============

> La única duda que tuvimos es que por lo que entendimos en el problema, si los ratones ya están comiendo en el plato, y de momento llega un gato, este no puede comerselo debido a que es un ¿Caballero?, de cualquier forma, si este argumento es correcto, entonces créemos la forma en que abordamos el problema es correcta.
