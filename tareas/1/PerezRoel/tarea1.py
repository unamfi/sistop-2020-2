from threading import Semaphore, Thread
from time import sleep 
from random import randint

#Num max de alumnos con el asesor
x = 5
#Num max de preguntas por alumno
y = 10

cubiculo = Semaphore(x) 
profesor = Semaphore(1)

def alumno(id):
	preguntas_totales = randint(1,y)
	num_pregunta = 1
	cubiculo.acquire()
	print('El alumno %d ha entrado al cubiculo. Tiene %d preguntas' % (id, preguntas_totales))
	while(num_pregunta <= preguntas_totales):
		profesor.acquire()
		print('Alumno %d hace pregunta %d' % (id, num_pregunta))
		profesor.release()
		num_pregunta = num_pregunta + 1
	cubiculo.release()
	print('El alumno %d ha salido del cubiculo' % (id))


	def asesoria()


for i in range(1,50):
	t = Thread(target = alumno, args = [i])
	t.start()




