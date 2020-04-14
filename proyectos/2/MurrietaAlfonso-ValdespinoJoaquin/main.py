from threading import RLock, Thread 
from time import sleep

from modulos.agencia import agencia
from modulos.compania import compania
from modulos.cliente import cliente


lock = RLock()
lock.acquire()
lock.release()

hilosList = []

clienteList = []
companiaList = []
agenciaList = []


aereomar = compania('Aeromar')
aereomexico = compania('Aereomexico')
interjet = compania('InterJet')
volaris = compania('volaris')

companiaList = [aereomar,aereomexico,interjet,volaris]

coppel = agencia(companiaList,'coppelViajes')
despegar = agencia(companiaList, 'despegar.com')
mundo  = agencia(companiaList, "mundomex")
best = agencia(companiaList, 'bestday')
palacio = agencia(companiaList, 'viajesPalacio')

agenciaList = [coppel,despegar,mundo,best,palacio]

for agencias in agenciaList:
    agencias.run()

sleep(2)

for i in range(10):
    clienteList.append( cliente(agenciaList))
    hilosList.append(Thread(target=clienteList[i].run).start())