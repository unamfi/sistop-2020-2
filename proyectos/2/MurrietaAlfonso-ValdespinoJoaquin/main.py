from threading import RLock, Thread #RLock usado en caso de usar .acquiare por segunda vez desde el mismo hilo
from time import sleep

# Modulos propios ->Carpeta modulo
from modulos.agencia import agencia
from modulos.compania import compania
from modulos.cliente import cliente


if __name__ == "__main__":
    numClientes=4
    lock = RLock()
    lock.acquire()
    lock.release()

    hilosList = []
    clienteList = []
    companiaList = []
    agenciaList = []

    #Compañias de vuelo
    aereomar = compania('Aeromar')
    aereomexico = compania('Aereomexico')
    interjet = compania('InterJet')
    volaris = compania('volaris')
    companiaList = [aereomar,aereomexico,interjet,volaris]

    #Agencias de vuelo
    coppel = agencia(companiaList,'coppelViajes',numClientes)
    despegar = agencia(companiaList, 'despegar.com',numClientes)
    mundo  = agencia(companiaList, "mundomex",numClientes)
    best = agencia(companiaList, 'bestday',numClientes)
    palacio = agencia(companiaList, 'viajesPalacio',numClientes)
    agenciaList = [coppel,despegar,mundo,best,palacio]

    for agencias in agenciaList:
        agencias.run()

    sleep(2)

    # creando clientes y corriendo los hilos correspondientes
    for i in range(numClientes):
        clienteList.append( cliente(agenciaList))
        hilosList.append(Thread(target=clienteList[i].run).start())