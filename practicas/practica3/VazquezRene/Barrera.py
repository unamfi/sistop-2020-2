from threading import Thread, Semaphore
from time import sleep
from random import random

espera = 3
cuenta = 0
mutex = Semaphore(1)
barrera = Semaphore(0)

def vamos(id):
    global cuenta, mutex, barrera, espera
    inicializa(id)
    with mutex:
        cuenta = cuenta + 1
        print("   %d esperando" % cuenta)
        if cuenta == espera:
            print("-*- ¡Pasen!")
            cuenta = 0
            for i in range(espera):
                barrera.release()
    barrera.acquire()
    # barrera.release()
    procesa(id)

def inicializa(id):
    print("%d: inicializando" % id)
    sleep(random())
    print("%d: listo para trabajar" % id)

def procesa(id):
    print("%d: procesando" % id)

for i in range(30):
    Thread(target=vamos, args=[i]).start()