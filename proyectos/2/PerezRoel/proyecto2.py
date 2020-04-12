#El bufon en el trono

from threading import Semaphore, Thread
from time import sleep
from random import randint

N = 10 # Tolerancia de cortesanos que pasan
M = 5 # Tolerancia de cortesanos esperando

debeLevantarse = Semaphore(0) # Señalización
puedeSentarse = Semaphore(1) # 'Apagador' 
puertaCortesanos = Semaphore(1) # Torniquete
cederTrono = Semaphore(0) # Señalización
reyPresente = False 
bufonSentado = False 
cortesanosPasados = 0
cortesanosEsperando = 0
presentes = 0 # presentes en la sala, sin incluir al bufón
mutex = Semaphore(1) # Mutex para todas las variables. 


#Hilo del rey.
def rey():
	global presentes, reyPresente, bufonSentado
	while(True):

		if( randint(0,5) == 0 ):

			mutex.acquire()
			print("Ahi viene el rey!")
			reyPresente = True
			presentes += 1

			#Si es el primero, adquiere el apagador
			if presentes == 1 and not bufonSentado:
				puedeSentarse.acquire()

			#Si el bufón está sentado, le indica que se levante y le ceda el trono.
			if bufonSentado:
				debeLevantarse.release()
				puedeSentarse.acquire()####
				mutex.release()
				cederTrono.acquire()
			else:
				mutex.release()

			print("El rey se sienta en el trono.")
			sleep(randint(3,5))

			#El rey termina. Si es el último en salir, libera el apagador.
			mutex.acquire()
			presentes -= 1
			reyPresente = False
			print("El rey se levanta del trono y se va.")
			if presentes == 0:
				print("No hay moros en la costa!")
				puedeSentarse.release()
			mutex.release()

		sleep(1)

#Hilo del bufón.
def bufon():
	sleep(2)
	global reyPresente, bufonSentado, cortesanosPasados, cortesanosEsperando
	while(True):

		#Reinicia la cuenta de cortesanos que han pasado
		mutex.acquire()
		cortesanosPasados = 0
		mutex.release()

		#Procede cuando el apagador esté libre para sentarse
		print("El bufón espera pacientemente...")
		puedeSentarse.acquire()

		#Se sienta en el trono
		mutex.acquire()
		bufonSentado = True
		mutex.release()
		print("El bufón se sienta en el trono.")

		#Espera a que le señalicen que debe levantarse.
		debeLevantarse.acquire()

		#Cede el apagador.
		puedeSentarse.release()

		print("El bufón debe levantarse!")

		#Sale
		mutex.acquire()
		bufonSentado = False 

		#Si hay cortesanos en la puerta, libera el torniquete.
		if cortesanosEsperando >= M:
			print("El bufón abre la puerta. >:)")
			puertaCortesanos.release()

		#Si el rey llegó, le cede el trono. 
		if reyPresente:
			print("El bufón cede el trono al rey.")
			cederTrono.release()
		mutex.release()


#Hilo del cortesano. 
def cortesano(id):
	global presentes, cortesanosEsperando, cortesanosPasados, bufonSentado

	mutex.acquire()
	cortesanosEsperando += 1
	print("El cortesano %d está en la puerta. pr = %d, pa = %d, e = %d, " % (id, presentes, cortesanosPasados, cortesanosEsperando) )
	
	#El cortesano está afuera de la sala. Si ya son M esperando:
	if cortesanosEsperando == M:	
		print("Ya hay %d cortesanos esperando. Hay que abrirles la puerta!" % (M))
		#Si el bufón está sentado, se le señaliza que debe levantarse;
		#de lo contrario, se reinicia la cuenta y se libera el torniquete.
		if bufonSentado:
			debeLevantarse.release()
		else:
			print("El bufón abre la puerta. :(")
			cortesanosPasados = 0###
			puertaCortesanos.release()
	mutex.release()

	#Se pasa por el torniquete
	puertaCortesanos.acquire()
	puertaCortesanos.release()

	#Se actualiza presentes, cortesanosEsperando y cortesanosPasados. 
	#Si se es el primero en llegar y el bufón no está sentado, se adquiere al torniquete. 
	mutex.acquire()
	presentes += 1
	if presentes == 1 and not bufonSentado:
		puedeSentarse.acquire()
	cortesanosEsperando -= 1
	cortesanosPasados += 1

	print("El cortesano %d está en la sala. pr = %d, pa = %d, e = %d, " % (id, presentes, cortesanosPasados, cortesanosEsperando) )

	#Se entra a la sala
	#Si ya han pasado N cortesanos y el bufón no se ha sentado, se cierra el torniquete. 
	if cortesanosPasados == N and not bufonSentado:
		print("El bufón ya esperó demasiado. Cierra la puerta cuando nadie lo ve.")
		#cortesanosPasados = 0
		mutex.release()
		puertaCortesanos.acquire()
	else: 
		mutex.release()
	
	sleep(randint(5,10))

	#El cortesa sale.
	mutex.acquire()
	presentes -= 1
	print("El cortesano %d se retira. pr = %d, pa = %d, e = %d, " % (id, presentes, cortesanosPasados, cortesanosEsperando) )
	
	#Si es el último en retirarse y el bufón no está sentado, se libera al apagador.
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
