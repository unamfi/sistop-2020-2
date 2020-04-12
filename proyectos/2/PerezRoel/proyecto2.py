#El bufon en el trono

from threading import Semaphore, Thread
from time import sleep
from random import randint
import config as c

N = 10 # Tolerancia de cortesanos que pasan
M = 5 # Tolerancia de cortesanos esperando

debeLevantarse = Semaphore(0) # Señalización
puedeSentarse = Semaphore(1) # 'Apagador' 
puertaCortesanos = Semaphore(1) # Torniquete
cederTrono = Semaphore(0) # Señalización
cortesanosPasados = 0
reyPresente = False 
bufonSentado = False 
presentes = 0 # presentes en la sala, sin incluir al bufón
mutex = Semaphore(1) # Mutex para todas las variables. 
cortesanosEsperando = 0

#Variables que no sirven para concurrencia, sino para la visualización
puertaCerrada = False
reySentado = False

#Hilo del rey.
def rey():
	global presentes, reyPresente, bufonSentado, reySentado
	while(True):

		if( randint(0,5) == 0 ):

			mutex.acquire()
			presentes += 1
			reyPresente = True

			#print("Ahi viene el rey!")
			actualizarSinMutex("Ahi viene el rey!")

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

			mutex.acquire()
			reySentado = True
			actualizarSinMutex("El rey se sienta en el trono.")
			mutex.release()
			sleep(randint(3,5))

			#El rey termina. Si es el último en salir, libera el apagador.
			mutex.acquire()
			presentes -= 1
			reySentado = False
			reyPresente = False

			actualizarSinMutex("El rey se levanta del trono y se va.")

			if presentes == 0:
				actualizarSinMutex("No hay moros en la costa!")
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
		actualizarSinMutex("El bufón espera pacientemente...")
		puedeSentarse.acquire()

		#Se sienta en el trono
		mutex.acquire()
		bufonSentado = True
		actualizarSinMutex("El bufón se sienta en el trono.")
		mutex.release()

		#Espera a que le señalicen que debe levantarse.
		debeLevantarse.acquire()

		#Cede el apagador.
		puedeSentarse.release()

		#print("El bufón debe levantarse!")

		#Sale
		mutex.acquire()
		actualizarSinMutex("El bufón debe levantarse!")
		bufonSentado = False 

		#Si hay cortesanos en la puerta, libera el torniquete.
		if cortesanosEsperando >= M:
			puertaCerrada = False
			actualizarSinMutex("El bufón abre la puerta. >:)")
			puertaCortesanos.release()

		#Si el rey llegó, le cede el trono. 
		if reyPresente:
			actualizarSinMutex("El bufón cede el trono al rey.")
			cederTrono.release()
		mutex.release()


#Hilo del cortesano. 
def cortesano(id):
	global presentes, cortesanosEsperando, cortesanosPasados, bufonSentado, puertaCerrada

	mutex.acquire()
	cortesanosEsperando += 1

	#print("El cortesano %d está en la puerta. pr = %d, pa = %d, e = %d, " % (id, presentes, cortesanosPasados, cortesanosEsperando) )
	actualizarSinMutex("El cortesano "+str(id)+" está en la puerta.")


	#El cortesano está afuera de la sala. Si ya son M esperando:
	if cortesanosEsperando == M:	
		#print("Ya hay %d cortesanos esperando. Hay que abrirles la puerta!" % (M))
		actualizarSinMutex('Ya hay '+str(M)+' cortesanos esperando. Hay que abrirles la puerta!')
		#Si el bufón está sentado, se le señaliza que debe levantarse;
		#de lo contrario, se reinicia la cuenta y se libera el torniquete.
		if bufonSentado:
			debeLevantarse.release()
		else:
			cortesanosPasados = 0
			puertaCerrada = False
			actualizarSinMutex("El bufón abre la puerta. :(")
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

	actualizarSinMutex("El cortesano "+str(id)+" está en la sala.")

	#Se entra a la sala
	#Si ya han pasado N cortesanos y el bufón no se ha sentado, se cierra el torniquete. 
	if cortesanosPasados == N and not bufonSentado:
		puertaCerrada = True
		actualizarSinMutex("El bufón ya esperó demasiado. Cierra la puerta cuando nadie lo ve.")
		#cortesanosPasados = 0
		mutex.release()
		puertaCortesanos.acquire()
	else: 
		mutex.release()
	
	sleep(randint(5,10))

	#El cortesa sale.
	mutex.acquire()
	presentes -= 1
	actualizarSinMutex("El cortesano "+str(id)+" se retira.")
	
	#Si es el último en retirarse y el bufón no está sentado, se libera al apagador.
	if presentes == 0 and not bufonSentado:
		actualizarSinMutex("No hay moros en la costa!")
		puedeSentarse.release()
	mutex.release()


def llegadaCortesanos():
	i = 1
	while(True):
		if(randint(0,1) == 0):
			Thread(target = cortesano, args = [i]).start()
			i += 1
		sleep(1)


def actualizarSinMutex(msg):

	global puertaCerrada, reyPresente, reySentado, bufonSentado, presentes

	if c.vis:
		c.grafico[0] = "  " + ("C"*cortesanosEsperando) + (" "*(20-cortesanosEsperando))
		
		if puertaCerrada:
			c.grafico[1] = "o====================o" 
		else:
			c.grafico[1] = "o=  =================o"

		if reyPresente:
			if reySentado:
				c.grafico[2] = "|       |  K  |       "
			else: 
				c.grafico[2] = "|       |     |      K"
		else: 
			c.grafico[2] = "|       |     |       "

		if bufonSentado:
			c.grafico[3] = "|       |  B  |      |"
		else:
			c.grafico[3] = "|       |     |   B  |"

		cortesanosPresentes = presentes
		if reyPresente:
			cortesanosPresentes -= 1
		c.grafico[5] = "| " + (cortesanosPresentes*"C") + ((19-cortesanosPresentes)*" ") + "|"
		
		c.grafico[7] = msg


		#Rendevouz para refrescar la pantalla
		c.sigHilos.release()
		c.sigInterfaz.acquire()

	else:
		sleep(0)



def actualizarConMutex():
	print("Hola")



"""
Thread(target = rey, args = []).start()
Thread(target = bufon, args = []).start() 
"""
