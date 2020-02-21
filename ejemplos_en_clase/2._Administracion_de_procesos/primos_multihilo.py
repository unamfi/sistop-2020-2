#!/usr/bin/python3
import threading
import time

MAXIMO = 1000
HILOS = 4

def es_primo(x):
    for i in range(2, x-1):
        if x % i == 0:
            return False
    return True

def prueba_rango(min,max, hilo):
    for i in range(min, max):
        if es_primo(i):
            print("%d: Encontré un nuevo primo: %d" % (hilo, i))
            time.sleep(0.005) # FUCHI, pero obliga al cambio de hilo

for i in range(1, HILOS+1):
    bloque = MAXIMO//HILOS
    t = threading.Thread(target=prueba_rango,
                         args=[bloque * (i-1) + 1,
                               bloque * i,
                               i ])
    t.start()

