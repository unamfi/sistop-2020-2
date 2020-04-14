#!/usr/bin/python3
from threading import Semaphore, Thread
from random import randint
from time import sleep

lugares = Semaphore(5)
alumnos_a_bordo = []
total_alumnos=20

def proviene():
    return randint(1,5)

def destino(este_no):
    dest = randint(1,5)
    while dest == este_no:
        dest = randint(1,5)
    return dest

def elevador():
    llevados=0
    while(True):
        for i in alumnos_a_bordo:
            print("Llevando a alumno ",i[0]," del piso ",i[1]," al piso ",i[2],". Hay ",len(alumnos_a_bordo)," a bordo")
            alumnos_a_bordo.remove(i)
            llevados+=1
            
            lugares.release()
            print("estado de semaforo: ",lugares._value,"\n\n")
            if(llevados==total_alumnos):
                return
    

def alumno(num):
    vengo_de = proviene()
    voy_a = destino(vengo_de)
    print('El alumno %d viene de %d y va a %d \n' % (num, vengo_de, voy_a))

    lugares.acquire()

    alumnos_a_bordo.append([num,vengo_de,voy_a])

for i in range(1,total_alumnos+1):
    t = Thread(target = alumno, args = [i])
    t.start()

e = Thread(target = elevador, args = [])
e.start()

