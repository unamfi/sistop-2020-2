#El bufon en el trono

from threading import Semaphore, Thread
from time import sleep
from random import randint

N = 10
M = 5

debeLevantarse = Semaphore(0) # Señalización
puedeSentarse = Semaphore(1) # Apagador 
puertaCortesanos = Semaphore(1) # Turnstile
cederTrono = Semaphore(0) # Señalización
reyPresente = False 
bufonSentado = False 
cortesanosPasados = 0
cortesanosEsperando = 0
presentes = 0
mutex = Semaphore(1) # Mutex para todas las variables. 

def rey():
	global presentes, reyPresente, bufonSentado
	while(True):
		if( randint(0,5) == 0 ):

			mutex.acquire()
			print("Ahi viene el rey!")
			reyPresente = True
			presentes += 1
			if presentes == 1 and not bufonSentado:
				puedeSentarse.acquire()
			if bufonSentado:
				debeLevantarse.release()
				puedeSentarse.acquire()####
				mutex.release()
				cederTrono.acquire()
			else:
				mutex.release()

			print("El rey se sienta en el trono.")
			sleep(randint(3,5))

			mutex.acquire()
			presentes -= 1
			reyPresente = False
			print("El rey se levanta del trono y se va.")
			if presentes == 0:
				print("No hay moros en la costa!")
				puedeSentarse.release()
			mutex.release()

		sleep(1)

def bufon():
	sleep(2)
	global reyPresente, bufonSentado, cortesanosEsperando
	while(True):
		print("El bufón espera pacientemente...")
		puedeSentarse.acquire()

		mutex.acquire()
		bufonSentado = True
		mutex.release()
		print("El bufón se sienta en el trono.")

		debeLevantarse.acquire()
		puedeSentarse.release()

		print("El bufón debe levantarse!")

		mutex.acquire()
		bufonSentado = False 
		if cortesanosEsperando >= M:
			print("El bufón abre la puerta. >:)")
			puertaCortesanos.release()
		if reyPresente:
			print("El bufón cede el trono al rey.")
			cederTrono.release()
		mutex.release()



def cortesano(id):
	global presentes, cortesanosEsperando, cortesanosPasados, bufonSentado

	mutex.acquire()
	cortesanosEsperando += 1
	print("El cortesano %d está en la puerta. pr = %d, pa = %d, e = %d, " % (id, presentes, cortesanosPasados, cortesanosEsperando) )
	if cortesanosEsperando == M:
		print("Ya hay %d cortesanos esperando. Hay que abrirles la puerta!" % (M))
		if bufonSentado:
			debeLevantarse.release()
		else:
			print("El bufón abre la puerta. :(")
			puertaCortesanos.release()
	mutex.release()

	puertaCortesanos.acquire()
	puertaCortesanos.release()

	mutex.acquire()
	presentes += 1
	if presentes == 1 and not bufonSentado:
		puedeSentarse.acquire()
	cortesanosEsperando -= 1
	cortesanosPasados += 1

	print("El cortesano %d está en la sala. pr = %d, pa = %d, e = %d, " % (id, presentes, cortesanosPasados, cortesanosEsperando) )

	if cortesanosPasados == N and not bufonSentado:
		print("El bufón ya esperó demasiado. Cierra la puerta cuando nadie lo ve.")
		cortesanosPasados = 0
		mutex.release()
		puertaCortesanos.acquire()
	else: 
		mutex.release()
	
	sleep(randint(5,10))

	mutex.acquire()
	presentes -= 1
	print("El cortesano %d se retira. pr = %d, pa = %d, e = %d, " % (id, presentes, cortesanosPasados, cortesanosEsperando) )
	if presentes == 0 and not bufonSentado:
		print("No hay moros en la costa!")
		puedeSentarse.release()
	mutex.release()


Thread(target = rey, args = []).start()
Thread(target = bufon, args = []).start() 


i = 1
while(True):
	if(randint(0,1) == 0):
		Thread(target = cortesano, args = [i]).start()
		i += 1
	sleep(1)
