Javier Loidi Gutiérrez - Sistemas Operativos

TAREA 1

-----------------------------------------------------

Problema a resolver: Elevador

-----------------------------------------------------

Lenguaje en el que se desarrolló: Python 3

-----------------------------------------------------

Estrategia utilizada:

Para la resolución del problema utilicé un Multiplex que solamente
deje utilizar cinco hilos a la vez, estos hilos logicamente son los
alumnos que abordarán el elevador.

También implementé Señalización ya que el hilo del elevador hace un
release() de los semaforos que hicieron acquire() en los hilos
correspondientes a los alumnos.

-----------------------------------------------------

No implementé refinamientos

-----------------------------------------------------
