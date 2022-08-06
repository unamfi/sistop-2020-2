# -*- coding: utf-8 -*-

import threading
import random

numViajes = 20
totalAsientos = 4

mutexBalsa = threading.Semaphore(1)
fila = threading.Semaphore(1)


def linux():
	global linuxProg

	mutexBalsa.acquire() 		#Se añaden 
	tomaAsiento('Linux')
	mutexBalsa.release()


def microsoft():
	global microsoftProg

	mutexBalsa.acquire()
	tomaAsiento('Microsoft')
	mutexBalsa.release()


def tomaAsiento(tipo):
	global totalAsientos
	
	totalAsientos = totalAsientos - 1
	print('El programador {} ha tomado asiento en la balsa'.format(tipo))
	print('Número de asientos restantes: {}'.format(totalAsientos))


def terminarViaje():
	global totalAsientos

	totalAsientos = 4
	print('Viaje terminado\n\n')


def main():

	fila.acquire()
	opciones = random.choice([0,1,2])
	if(opciones == 0):
		for i in range(4):
			linux()
	elif(opciones == 1):
		for i in range(2):
			linux()
			microsoft()
	else:
		for i in range(4):
			microsoft()


	fila.release()
	terminarViaje()
	


for i in range(numViajes):
	a = threading.Thread(target = main)
	a.start()

