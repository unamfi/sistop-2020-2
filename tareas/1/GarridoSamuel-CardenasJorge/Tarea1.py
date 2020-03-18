import threading as thrd
from threading import Semaphore
import random
import time
from concurrent.futures.thread import ThreadPoolExecutor
print("Tom, Jerry y sus amigos")

##Pedimos el número de gatos, platos y ratones al usuario
gatoInput = int(input("Ingrese el número de gatos: "))

ratonInput = int(input("Ingrese el número de ratones: "))

platosInput = int(input("Ingrese el número de platos: "))


#Necesitamos los semáforos que nos indicarán la posibilidad de que haya gatos y ratones en la habitación

ratones = 0
gatos = 0
ratonMutex = Semaphore(1)
gatoMutex = Semaphore(1)
platos = Semaphore(platosInput)

#El apagador ya que si un gato come un ratón no puede entrar 
Apagador = Semaphore(1)

#Haremos una lista para mostrar al final
listaVivos = []
listaMuertos = []

#Función de comer o que coman al ratón si un gato entra en escena
def comeRaton(id):
    global ratones, gatos
    platos.acquire() # Agarra un plato
    ratonMutex.acquire()
    ##Enciende la alarma de que ratones están comiendo y ya no llegan gatos
    ratones = ratones + 1
    if ratones == 1:
        Apagador.acquire()
    ratonMutex.release()

    print("Ratón ",id," está comiendo en el plato ",int(platos._value))  
    ##Liberamos al mutex del ratón para indicar que pueden ingresar gatos pero ahora los gatos pueden entrar
    gatoMutex.acquire()
    ##Si llega a entrar un comerGato()

    if(gatos > 0):
        print("Un gato ha entrado a comer en el plato", int(platos._value))
        print("❌ El gato se ha comido al ratón",id)
        listaMuertos.append(id)
    else:
        print("Acabó de comer el ratón ",id)
        listaVivos.append(id)
    ## En caso que no se encuentren ambos podemos liberar
    gatoMutex.release()
    ratonMutex.acquire()
    ratones-=1

    #En caso que ya no haya ratones por alimentar liberamos los mutexs
    if ratones == 0:
        Apagador.release()
        
    ratonMutex.release()
    platos.release()

def comeGato(id):
    global gatos
    Apagador.acquire()
    Apagador.release()
    ## Esto para que pueda ser posible que entren "accidentalmente los ratones"
    platos.acquire()
    ## Bajamos el número de platos disponibles
    print("Gato",id, "está comiendo")        
    gatoMutex.acquire()
    ## Entra un gato por lo que por caballero informa que está presente
    gatos = gatos + 1
    time.sleep(random.random()) #Espera
    gatoMutex.release()
    print("El gato",id,"ha terminado de comer")
    gatoMutex.acquire()
    gatos = gatos - 1
    ## Se retira la advertencia
    gatoMutex.release()
    platos.release()
    ##Liberamos los demás


def ContabilidadFinal():
    ##Realizamos una contabilidad final de los pobres ratones caídos en batalla
    print("\n🐭🐭 Los marcadores al final: 🐭🐭")
    print("\nRatones Vivos: ")
    for x in listaVivos:
        print("Ratón: ",x)
    print("\nRatones Muertos: ")
    for y in listaMuertos:
        print("Ratón: ",y)


## Lanzamos los hilos de los gatos
for i in range(gatoInput):
    thrd.Thread(target=comeGato, args=[i+1]).start()

## Lanzamos los hilos de los ratones
for i in range(ratonInput):
    thrd.Thread(target=comeRaton, args=[i+1]).start()

## Esperamos que todo termine enumerando todos los hilos y hasta que hagan join lanzaremos el marcador
for thread in thrd.enumerate():
    if thread.daemon:
        continue
    try:
        thread.join()
    except RuntimeError as err:
        if 'cannot join current thread' in err.args[0]:
            continue
        else:
            raise

ContabilidadFinal()
