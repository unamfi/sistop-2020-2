"""
Ejercicio de sincronización
Alumnos y Asesor
"""

from threading import Thread,Semaphore
from random import random, randrange
import time

lugar=Semaphore(5)#Lugares disponibles
mutex=Semaphore(1)#Mutex para realizar preguntas
alumnos=0#Cantidad de alumnos actuales en la sala
def sesionAsesor(id, lugar, preguntas,hechas):
	global alumnos
	
	if(alumnos==0):
		print('El profesor esta acostado en las sillas')
	lugar.acquire()
	print('<-------El Alumno '+str(id)+' entró a la oficina del asesor. Tiene '+str(preguntas)+ ' preguntas')
	alumnos+=1
	while(preguntas!=hechas):	
		mutex.acquire()
		print('El Alumno '+str(id)+' realizó una pregunta')
		hechas+=1
		mutex.release()
		time.sleep(random())
		
		if(preguntas==hechas):
			print('------->El alumno '+str(id)+' agradece al profesor y se retira')
			alumnos-=1			
		lugar.release()
		if(alumnos==0):
			print('El profesor esta acostado en las sillas')

for i in range (10):
	preguntas=randrange(1,4)
	hechas=0
	Thread(target=sesionAsesor, args=[i+1, lugar, preguntas, hechas]).start();



	"""
	Otras formas que realice con fallos
	
	#print (datos['name'])
	with lugar:
		if(alumnos!=sillas):
			print('Se sentó '+datos['name']+' Tiene '+str(datos['preguntas'])+' preguntas')
			##while(datos['preguntas']!=datos['preguntasHechas']):
				
			alumnos+=1
			
			while(datos['preguntasHechas']!=datos['preguntas']):
				mutex.acquire()
				print(datos['name']+' realizó una pregunta')
				time.sleep(random())
				datos['preguntasHechas']+=1
				mutex.release()
				if(datos['preguntas']==datos['preguntasHechas']):
					salida.release()
					print(datos['name']+' agradece al asesor y se retira')
					alumnos-=1

		






	
	print('Se sentó '+datos['name']+' Tiene '+str(datos['preguntas'])+' preguntas')
	alumnos+=1
			
	while(alumnos!=sillas or alumnos!=0):
	
		mutex.acquire()
		print(datos['name']+' realizó una pregunta')
		datos['preguntasHechas']+=1
		mutex.release()
		if(datos['preguntas']==datos['preguntasHechas']):
			print(datos['name']+' agradece al asesor y se retira')
			salida.release()
			alumnos-=1


#Asignación de nombre, preguntas hechas y preguntas realizadas
def alumno(i, **datos):
	nombre=datos['name']
	preguntas=datos['preguntas']
	preguntasHechas=datos['preguntasHechas']

for i in range(10):
	Thread(target=sesionAsesor,args={i,}, kwargs={'name':'Alumno %s '%i,'preguntas':randrange(2,5), 'preguntasHechas':0}).start()"""