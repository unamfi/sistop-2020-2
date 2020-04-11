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
chefsDisponibles = []

## Mutex para los chefs y meseros disponibles y fila de clientes en espera
mutex_fila_espera = threading.Semaphore(1)
mutex_meseros_disp = threading.Semaphore(1)
mutex_chefs_disp = threading.Semaphore(1)

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
        self.esperarComida = True
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
        while self.esperarComida == True:
            print("Yo, el cliente {}, estoy esperando nuestra orden".format(self.id_cliente))
        self.comer()
        self.llamarMesero("cuenta")
        self.irse()

        mesas.release()
    
    def llamarInvitado(self,i):
        return threading.Thread(target = Cliente.Invitado, args=[self, i]).start()

    def llamarMesero(self, peticion):
        global meserosDisponibles, meseros, mutex_meseros_disp
        print("el cliente {} tiene una petición".format(self.id_cliente))

        #se pide un mesero, se saca de la lista de disponibles, se le da la peticion
        #al completar la acción el mesero regresa a estar disponible
        meseros.acquire()
        mutex_meseros_disp.acquire()
        mesero = meserosDisponibles.pop(0)
        mutex_meseros_disp.release()
        mesero.activar(peticion, self.id_cliente, self)
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
        


class Invitado:
    def __init__(self,cliente,id_invitado):
        self.cliente = cliente
        self.id_invitado = id_invitado
        self.leerMenu()
        self.decidirOrden()

    def leerMenu(self)
        print("El invitado {} del cliente {} leé el menu".format(self.id_invitado,self.cliente.id_cliente))
        espera = random.randrange(1,5)
        for i in range(espera):
            pass

    def decidirOrden(self):
        self.cliente.mutex_orden.acquire()
        #mensaje 
        #tiempo espera
        self.cliente.cuenta_orden += 1
        self.cliente.mutex_orden.release()
        self.cliente.lista_invitados.append(self)

    def comer(self):
        #t espera
        self.cliente.mutex_comer.acquire()
        #mensaje de que termino
        self.cliente.barrera_comer += 1
        self.cliente.mutex_comer.release()


class Mesero:
    def __init__(self, id_mesero):
        self.id_mesero = id_mesero
        self.descansar = threading.Semaphore(0)
        #*
        self.enlistar()

    def enlistar(self):
        global meserosDisponibles
        mutex_meseros_disp.acquire()
        meserosDisponibles.append(self)
        mutex_meseros_disp.release()

    def activar(self, peticion, id_cliente, cliente, cliente):
        global mutex_meseros_disp, meserosDisponibles
        self.descansar.release()

       if peticion == "mesa":
             self.llevarMesa(id_cliente)
        elif peticion == "menu":
             self.mostrarMenu(id_cliente)
        elif peticion == "orden":
             self.llevarOrdenAChef(id_cliente, cliente)
        elif peticion == "ordenLista":
             self.llevarOrdenAMesa(id_cliente, cliente)
        elif peticion == "cuenta":
             self.traerCuenta(id_cliente)

        print("El mesero {} ya se encuentra libre".format(self.id_mesero))
        self.enlistar

    def llevarMesa(self, id_cliente):
        print("Yo, el mesero {}, llevare al cliente {} a su mesa".format(self.id_mesero,id_cliente))

    def mostrarMenu(self, id_cliente):
        print("Yo, el mesero {}, le he dado los Menus a todos en la mesa del cliente {} ".format(self.id_mesero,id_cliente))

    def llevarOrdenAChef(self, id_cliente, cliente):
        global chefsDisponibles, chefs, mutex_chefs_disp
        print("Yo, el mesero {}, he llevado la orden del cliente {} a preparar".format(self.id_mesero,id_cliente))


        #se pide un chef, se saca de la lista de disponibles
        #al completar la acción el chef regresa a estar disponible
        chefs.acquire()
        mutex_chefs_disp.acquire()
        chef = chefsDisponibles.pop(0)
        mutex_chefs_disp.release()
        chef.cocinar(cliente)
        chefs.release()

    def llevarOrdenAMesa(self, id_cliente, cliente):
        print("Yo, el mesero {}, llevo la orden lista del cliente {} ".format(self.id_mesero,id_cliente))
        cliente.esperarComida = False

    def traerCuenta(self, id_cliente)
        print("Yo, el mesero {}, llevo la cuenta en la mesa del cliente {} ".format(self.id_mesero,id_cliente))


class Chef:
    def __init__(self, id_chef):
        self.id_chef = id_chef
        self.enlistar()
    
    def enlistar(self):
        global chefsDisponibles
        mutex_chefs_disp.acquire()
        chefsDisponibles.append(self)
        mutex_chefs_disp.release()

    def cocinar(self, cliente):
        print("Yo, el chef {}, preparo la orden del cliente {} ".format(self.id_chef,cliente.id_cliente))
        espera = random.randrange(1,5)
        for i in range(espera):
            pass
        print("Yo, el chef {}, termine la orden del cliente {} ".format(self.id_chef,cliente.id_cliente))
        
        #busquemos un mesero que lleve la orden
        meseros.acquire()
        mutex_meseros_disp.acquire()
        mesero = meserosDisponibles.pop(0)
        mutex_meseros_disp.release()
        mesero.activar("ordenLista", cliente.id_cliente, cliente)
        meseros.release()

        print("Yo, el chef {}, estoy libre, ire a dormir".format(self.id_chef))
        self.enlistar()



class Restaurante:
