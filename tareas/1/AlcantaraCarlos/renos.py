# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:31:17 2020

@author: carlo
"""

from threading import Semaphore, Thread
from random import randint
from time import sleep


NUM_RENOS=9
NUM_ELFOS=500
NUM_ELFOS_ATENDIDOS=3
NUM_RENOS_NECESARIOS=9

numDuendes=0
numRenos=0

barreraRenos = Semaphore(0)
nRenosMutex=Semaphore(1)

entregaRegalos=False
santaWakeUp=Semaphore(0)

ayudaDuende=Semaphore(0)
mutexDuendes=Semaphore(1)



def santa():
    print('Descansaré hasta que me despierten')
    santaWakeUp.acquire()
    while True:
        if entregaRegalos==True:
            print('***Son %d renos, Es hora de entregar los regalos'%NUM_RENOS_NECESARIOS)
            break
        else:
            print('***Esta bien, les ayudaré duendes')
            print('***Ya regresaré a dormir')
            santaWakeUp.acquire()
    print('***Hemos terminado aqui, bai')
 

def reno(i):
    global numRenos,entregaRegalos
    print('+++Hola soy reno %d, voy a irme de vacaciones, regreso pronto'%(i) )
    vacaciones=randint(10,50)
    sleep(vacaciones)
    print('+++soy reno %d, ya volvi'%i)
    
    nRenosMutex.acquire()
    numRenos=numRenos+1
    if numRenos==NUM_RENOS_NECESARIOS:
        for x in range (1,NUM_RENOS_NECESARIOS):
            barreraRenos.release()
        numRenos=0
    nRenosMutex.release()
    barreraRenos.acquire()
    entregaRegalos=True
    santaWakeUp.release()
    
    
def elfo(i):
    global numDuendes
    print ('---Hola, soy elfo %d, estoy trabajando'%i)
    problema=randint(10,45)
    sleep(problema)
    print('---Hey soy elfo %d y tengo un problema'%i)

    mutexDuendes.acquire()
    numDuendes=numDuendes+1
    print('Duendes con problemas: %d'% numDuendes)
    if numDuendes==NUM_ELFOS_ATENDIDOS:
        for x in range (1,NUM_ELFOS_ATENDIDOS):
            ayudaDuende.release()
        numDuendes=0
        print('---Somos 3 duendes, Despertemos a santa')
        santaWakeUp.release()
    mutexDuendes.release()
    ayudaDuende.acquire()
    
    

t=Thread(target=santa)   
t.start()
   
for x in range(0,NUM_RENOS):
    t=Thread(target = reno, args = [x])
    t.start()

for x in range(0,NUM_ELFOS):
    t=Thread(target = elfo, args = [x])
    t.start()

