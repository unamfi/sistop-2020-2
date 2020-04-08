import threading
import random

#####################Variables globales########################

#meseros, chefs, mesas, clientes
num_meseros
num_mesas
num_chefs
num_clientes

###########listas
meserosDisponibles = []
clientesEnEspera = [] 

## Mutex para los meseros disponibles y fila de clientes en espera
mutex_fila_espera = threading.Semaphore(1)
mutex_meseros_disp = threading.Semaphore(1)

## Multiplex para chefs, mesa, meseros disponibles
chefs = threading.Semaphore(num_chefs)
meseros = threading.Semaphore(num_meseros)
mesas = threading.Semaphore(num_mesas)





#####################Clases######################################
class Cliente:
    def __init__(self, id_cliente, num_invitados):
        self.id_cliente = id_cliente
        self.num_invitados = num_invitados
        self.lista_invitados = []
        #usaremos una barrera para que todos elijan su platillo
        self.cuenta_orden = 0
        self.mutex_orden = threading.Semaphore(1)
        self.barrera_orden = threading.Semaphore(0)
        #usaremos una barrera para que todos terminen de comer
        self.cuenta_comer = 0
        self.mutex_comer = threading.Semaphore(1)
        self.barrera_comer = threading.Semaphore(0)

        self.esperarMesa()

    def esperarMesa(self):
        global mesas, mutex_fila_espera, clientesEnEspera
        #se adquiere una mesa, cuando la adquiere se saca de la lista
        mesas.acquire()
        mutex_fila_espera.acquire()
        clientesEnEspera.pop(0)
        mutex_fila_espera.release()

        self.llamarMesero("mesa")
        self.obtenerMesa()
        self.llamarMesero("menu")
        self.leerMenuYOrdenar()
        self.llamarMesero("orden")
        self.comer()
        self.llamarMesero("cuenta")
        self.irse()

        mesas.release()
    
    def llamarInvitado(self,i):
        return threading.Thread(target = Cliente.Invitado, args=[self, i]).start()

    def llamarMesero(self, peticion):
        global meserosDisponibles, meseros, mutex_meseros_disp, num_meseros
        print("el cliente {} tiene una petición".format(self.id_cliente))

        #se pide un mesero, se saca de la lista de disponibles, se le da la peticion
        #al completar la acción el mesero regresa a estar disponible
        meseros.acquire()
        mutex_meseros_disp.acquire()
        mesero = meserosDisponibles.pop(0)
        mutex_meseros_disp.release()
        mesero.activar(peticion, self.id_cliente)
        meseros.release()

    def obtenerMesa(self):
        print("Yo, el cliente {}, consegui una mesa para {} personas".format(self.id_cliente,self.num_invitados+1))

    def leerMenu(self):
        print("Yo, el cliente {}, estoy escogiendo mi platillo".format(self.id_cliente))
        espera = random.randrange(1,5)
        for i in range(espera):
            pass

    def decidirOrden(self):
        self.mutex_orden.acquire()
        print("Yo, el cliente {}, ya decidí qué ordenar".format(self.id_cliente))
        self.cuenta_orden += 1
        self.mutex_orden.release()


    def leerMenuYOrdenar(self):
        self.leerMenu()
        self.decidirOrden()
        acabar = True
        hilos = self.num_invitados + 1
        #aqui mandaremos a llamar a los invitados del cliente
        for i in range(self.num_invitados):
            self.llamarInvitado(i)
        #Barrera para esperar a que todos esten listos para ordenar
        while acabar:
            if self.cuenta_orden == hilos:
                self.barrera_orden.release()
                acabar = False
            
        print("todos en la mesa del cliente {} estan listos para ordenar".format(self.id_cliente))
        self.mutex_orden.acquire()
        self.mutex_orden.acquire()


    def comer(self):
        hilos = self.num_invitados + 1
        acabar = True
        espera = random.randrange(1,5)
        for i in range(espera):
            pass
        print("El cliente {} ha terminado de comer".format(self.id_cliente))
        #Hagamos que los invitados coman tambien
        for i in self.lista_invitados:
            i.comer()
        #barrera pa no ser descortes y esperar a que todos terminen de comer
        while acabar:
            if self.cuenta_comer == hilos:
                self.barrera_comer.release()
        self.barrera_comer.acquire()
        self.barrera_comer.release()

        print("todos en la mesa del cliente {} han terminado de comer".format(self.id_cliente))
        self.mutex_comer.acquire()
        self.mutex_comer.release()

    def irse(self):
        print("El cliente {} y sus {} invitados han decidido irse".format(self.id_cliente,self.num_invitados))
        











class invitado:


class Mesero:



class Chef:


class Restaurante:
