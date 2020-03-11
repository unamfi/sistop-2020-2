#!/usr/bin/python3
from threading import Semaphore, Thread
from random import randint
from time import sleep

s12 = Semaphore(1)
s24 = Semaphore(1)
s13 = Semaphore(1)
s34 = Semaphore(1)

# Definiciones:
# ¿De dónde y hacia dónde vamos?
#
#         1
#       |   |   |
#       |   |   |
#  -----+---+---+---
# 2     |   |   |
#  -----+---+---+---
#       |   |   |     3
#  -----+---+---+---
#       |   |   |
#       |   |   |
#       |   |   |
#             4

caminos = {
    1: { 2: [s12],
         3: [s12, s13, s34],
         4: [s12, s13]},
    2: { 1: [s13, s34, s24],
         3: [s13, s34],
         4: [s13]},
    3: { 1: [s24],
         2: [s24, s12],
         4: [s24, s12, s13]},
    4: { 1: [s34, s24],
         2: [s34, s24, s12],
         3: [s34]}
    }

def proviene():
    return randint(1,4)

def destino(este_no):
    dest = randint(1,4)
    while dest == este_no:
        dest = randint(1,4)
    return dest

def auto(num):
    vengo_de = proviene()
    voy_a = destino(vengo_de)
    print('El auto %d viene de %d y va a %d' % (num, vengo_de, voy_a))

    for i in caminos[vengo_de][voy_a]:
        i.acquire()
        print('El auto %d cruzando %s' % (num, i))
        sleep(0.025)
        i.release()

    print('El auto %d llegó a salvo a su destino.' % num)

for i in range(1,1000):
    t = Thread(target = auto, args = [i])
    t.start()
