# -*- coding: utf-8 -*-
from random import random
from time import sleep
import threading

dwarfs = 0
renos= 0
mutex = threading.Semaphore(1)
santa = threading.Semaphore(1)
torniquete = threading.Semaphore(1)


def reno(id):
    sleep(random())
    global renos
    print("Reno %d regresó del Caribe" % id)

    mutex.acquire()
    renos = renos + 1
    print("Reno %d: Ahora somos %d renos" % (id, renos))
    if renos == 9:
        mutex.release()
        torniquete.acquire()
        print("Reno %d:     ¡Hora de repartir regalos!" % id)
        santa.acquire()

        viaje()

        mutex.acquire()
        renos = 0
        print("     ¡Santa ha vuelto!")
        santa.release()
        torniquete.release()
        mutex.release()

def duende(id):
    sleep(random())
    global dwarfs
    print("   Duende %d: inicia, tiene un problema" % id)

    torniquete.acquire()
    torniquete.release()

    mutex.acquire()
    dwarfs = dwarfs + 1
    print("%d: Ahora somos %d dwarfs esperando" % (id, dwarfs))
    if dwarfs == 3:
        torniquete.acquire()
        print("%d: ¡Hora de ayuda de Santa!" % id)
        santa.acquire() 
        mutex.release()

        ayuda()

        print("%d:  Ya nos vamos, Santa ha vuelto a dormir." % id)
        mutex.acquire()
        dwarfs = 0
        torniquete.release()
        santa.release()
        mutex.release()

def ayuda():
    print(" ...Santa está ayudando a los dwarfs...")
    sleep(0.3)

def viaje():
    print(" ...Santa y los renos están fuera...")
    sleep(0.9)

for ren in range(9):
    threading.Thread(target = reno, args = [ren]).start()
for duen in range(20):
    threading.Thread(target = duende, args = [duen]).start()