#!/usr/bin/python3
'''
	Martinez Hernandez Niver Asaid

	Problema: Santa Claus

	Plateamiento:
	- Santa Claus duerme en el Polo Norte mientras sus elfos
	trabajan frenéticamente en la construcción de millones de
	nuevos juguetes
	- A veces se topan con un problema — Pueden pedir ayuda a
	Santa Claus, pero sólo de tres en tres.
	- Sus nueve renos pasan todo el año de vacaciones en las playas
	del Caribe
	- Santa debe despertar a tiempo para iniciar su viaje anual

	Reglas:
	Si los nueve renos están de vuelta, es hora de despertar a
	Santa Claus para que inicie su recorrido.
	Si los elfos tienen problemas construyendo algún juguete, le
	piden ayuda a Santa Claus
	- Pero para no darle demasiada lata, lo hacen sólo cuando hay
	tres elfos que tienen un problema. Mientras tanto, lo dejan
	dormir.
	- Puede haber cualquier cantidad de elfos.
'''

from threading import Semaphore, Thread
from time import sleep

santa = Semaphore(1)
semReno = Semaphore(0)
elfos = 0
renos = 0
torElfo = Semaphore(1)
mutex = Semaphore(1)
problema = 0

def syncSanta():
	while True:
		santa.acquire()
		print('Santa se levantó...')
		mutex.acquire()
		if renos >= 9:
			print('reno preparandose...')
			semReno.release()
			reno -= 9
		elif elfos == 3:
			print('ayudando elfos...')
		mutex.release()

def syncReno():
	while True:	
		mutex.acquire()
		reno += 1
		if renos == 9:
			santa.release()
		mutex.release()

		semReno.acquire()
		print('Los renos están listos para partir...')

def syncElfo():
	while True:
		#torElfo.acquire()
		#mutex.acquire()
		elfos += 1
		if elfos == 3:
			santa.release()
		else:
			torElfo.release()
		mutex.release()

		print('Santa ha atendiendo tres elfos...')

		mutex.acquire()
		elfos -= 1
		if elfos == 0:
			torElfo.release()
		mutex.release()

Thread(target=syncSanta, args=[]).start()
for i in range(20):
	t = Thread(target=syncElfo, args=[i])
	t.start()
for i in range(9):
	tr = Thread(target=syncReno, args=[i])