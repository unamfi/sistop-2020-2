"""
Permite manipular a los cocineros de una forma sencilla 
"""
from comun import Persona,siguiente_estado
from enum import Enum, unique
from threading import Thread
from random import random, randint 
from time import sleep 
from threading import Thread, Semaphore

class Linea_Orden:
    """
    Permite que los chefs tomen una orden y colocar una orden en servicio
    """

    def __init__(self):
        self.linea_entrada=[]
        self.mutex_entrada = Semaphore(1)
        self.mutex_disponibles_entrada = Semaphore(0)

    def colocar_orden_entrada(self,orden): ##Lo llama el mesero ##senalizacion y mutex
        self.mutex_entrada.acquire()
        self.linea_entrada.append(orden)
        self.mutex_disponibles_entrada.release()
        self.mutex_entrada.release()
    
    def obtener_orden_entrada(self):###Lo llama el chef
        self.mutex_disponibles_entrada.acquire()
        self.mutex_entrada.acquire()
        orden = self.linea_entrada.pop(0)
        self.mutex_disponibles_entrada.release()
        return orden


class Cocinero(Persona):
    """
    Representacion de un cocinero
    """
    servicio = None
    def __init__(self,id,estados,barra_pedidos):
        super.__init__(self,id,estados)
        self.orden = None
        self.barra_pedidos = barra_pedidos

    def encargar_orden(self,orden):
        self.orden = orden

    def terminar_turno(self,*arg,**args):
        pass

class Cocina:
    """
    Permite manipular a los cocineros de una forma sencilla

    Atributos:

    """
    def __init__(self, n):            
        '''
        Permite crear n cocineros:
        '''
        self.barra_pedidos = Linea_Orden()
        self.estados = EstadosCocinero(self.barra_pedidos)
        self.cocineros = []
        for i in range(n):
            self.cocineros.append(Cocinero(i,self.estados,self.barra_pedidos))

    def anadir_servicio(self,servicio):
        self.servicio = servicio
        Cocinero.servicio = servicio
    
    def start(self):
        for cocinero in self.cocineros:
            cocinero.start()
        cocinero.join()

    def anadir_orden(self,orden):
        self.barra_pedidos.colocar_orden_entrada(orden)

@unique
class EstadosCocinero(Enum):
    
     
    @siguiente_estado(siguiente = cocinar)
    def esperar_orden(self,this, *arg, **args):
        this.encargar_orden(this.barra_pedidos.obtener_orden_entrada())

        
    @siguiente_estado(siguiente = dejar_plato)
    def cocinar(self, this, *arg, **args):
        print("Cocinando")
        sleep(random() * 6 + .3)  # Simula que esta cocinando


    @siguiente_estado(siguiente=esperar_orden)
    def dejar_plato(self, this, *arg, **args):
        this.servicio.anadir_orden_lista(this.orden)
        this.orden=None

    
    inicial = esperar_orden
    def __str__(self):
        return str(self.name)

if __name__ == "__main__":
    pass