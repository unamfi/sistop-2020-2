# Tarea 1: Ejercicios de sincronizacion
# Los alumnos y el asesor
# por Roel Perez

from threading import Semaphore, Thread
from time import sleep 
from random import randint

x = 5 #Num max de alumnos en el cubículo
y = 5 #Num max de preguntas por alumno
Q = [] #Lista que almacena la pregunta (id y numero de pregunta)

cubiculo = Semaphore(x) #Multiplex de capacidad del cubículo
atencion = Semaphore(1) #Mutex de Q
preguntas = Semaphore(0) #Señalizador de que se ha hecho una pregunta
capacidad = Semaphore(1) #Mutex del proceso pregunta-respuesta

# hilo de alumno
def alumno(id):
	preguntas_totales = randint(1,y) #numero de preguntas que tiene el alumno 
	num_pregunta = 1 #contador del numero de pregunta
	cubiculo.acquire() #entra al cubiculo
	print('El alumno %d ha entrado al cubiculo. Tiene %d pregunta(s)' % (id, preguntas_totales))
	while(num_pregunta <= preguntas_totales): #mientras tenga preguntas no resueltas
		capacidad.acquire() # Adquiere el proceso de pregunta/respuesta
		atencion.acquire() # Escribe sobre la variable Q
		print('El alumno %d hace la pregunta %d' % (id, num_pregunta));
		Q.append(id)
		Q.append(num_pregunta)
		atencion.release()
		preguntas.release() #Señaliza al asesor que se hizo una pregunta
		num_pregunta += 1
		sleep(0.1)
	print('El alumno %d sale del cubiculo' % (id))
	cubiculo.release() #sale del cubiculo
	
def asesor():
	while(True):
		print('El asesor espera...')
		preguntas.acquire() # Espera a que hayan hecho una pregunta
		atencion.acquire() # Lee y limpia la variable Q  
		alumno_id = Q.pop(0)
		num_pregunta = Q.pop(0)
		print('El asesor responde la pregunta %d del alumno %d' % (num_pregunta,alumno_id))
		atencion.release() 
		capacidad.release() #Libera el proceso de pregunta/respuesta
		
#Se inicia un hilo de asesor
t_asesor = Thread(target = asesor)
t_asesor.start()

#Se inician 20 hilos de alumnos
for i in range(1,21):
	t_alumnos= Thread(target = alumno, args = [i])
	t_alumnos.start()
