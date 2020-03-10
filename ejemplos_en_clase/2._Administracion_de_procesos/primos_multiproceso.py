#!/usr/bin/python3
import os

MAXIMO = 1000

def es_primo(x):
    for i in range(2, x-1):
        if x % i == 0:
            return False
    return True

def prueba_rango(min,max):
    for i in range(min, max):
        if es_primo(i):
            print("Encontré un nuevo primo: %d" % i)

pid = os.fork()
repid = os.fork()
if pid == 0 and repid == 0:
    prueba_rango(1, MAXIMO//4)
elif pid == 0:
    prueba_rango(MAXIMO//4+1, MAXIMO//2)
elif repid == 0:
    prueba_rango(MAXIMO//2+1, MAXIMO//2+MAXIMO//4)
else:
    prueba_rango(MAXIMO//2+MAXIMO//4+1, MAXIMO)

# for i in range(1, 100):
#     if es_primo(i):
#         print("Encontré un nuevo primo: %d" % i)
