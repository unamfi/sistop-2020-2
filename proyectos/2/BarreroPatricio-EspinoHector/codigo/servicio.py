"""
Contiene clases necesarias para facilitar el trabajo con servicio
"""
from comun import Persona, siguiente_estado
from menu import Orden

from threading import Thread, Semaphore
from enum import Enum
from random import random
from time import sleep

class Mesa:
    """
    Representa el concepto de una mesa     
    
    Atributos:        
    disponibilidad (int): tiene valores verdadero o falso indicando si la mesa esta disponible o no.  
    numero_mesa (int): El numero de la mesa
    
    """
    def __init__(self, numero_mesa):
        self.numero_mesa = numero_mesa
        self.mutex_mesa = Semaphore(1)
        self.disponibilidad = True
        self.grupo = None
    def desocupar_mesa(self):
        self.mutex_mesa.acquire()
        self.disponibilidad = True
        self.grupo = None
        self.mutex_mesa.release()

    def ocupar_mesa(self, grupo):
        self.mutex_mesa.acquire()
        self.disponibilidad = False
        self.grupo = grupo
        self.mutex_mesa.release()

    def esta_disponible(self):
        self.mutex_mesa.acquire()
        disponibilidad = self.disponibilidad
        self.mutex_mesa.release()
        return disponibilidad

    def __str__(self):
        return str(self.numero_mesa)
class EstadosMesero(Enum):

    def disponible(self, this, *arg, **argv):
        this.servicio.semaforo_meseros.release()
        this.senalizador.acquire()

    def ocupado(self, this, *arg, **argv):
        pass

    @siguiente_estado(siguiente = disponible)
    def tomar_orden(self, this, *arg, **argv):
        this.mesa.grupo.senalador.release()  # Simula

    @siguiente_estado(siguiente = disponible)
    def atender_mesa(self, this, *arg, **argv):
        this.mesa.grupo.senalador.release()  # Simula atender a una mesa

    
    @siguiente_estado(siguiente = disponible)
    def llevar_comida(self, this, *arg, **argv):
        this.servicio.obtener_orden_cola()  # Simula obtener la comida
        this.mesa.grupo.senalador.release()  # Simula llevar la comida

    inicial = disponible

    def __str__(self):
        return str(self.name)

class Mesero(Persona):
    def __init__(self, id, servicio):
        super().__init__(id, EstadosMesero)
        self.senalizador = Semaphore(0)
        self.servicio = servicio
        self.mutex_estado = Semaphore(1)

    def siguiente_estado(self, estado):
        self.mutex_estado.acquire()
        self.estado = estado
        self.mutex_estado.release()

    def esta_disponible(self):
        self.mutex_estado.acquire()
        disponible = self.estado == EstadosMesero.disponible
        self.mutex_estado.release()
        return disponible

class Servicio(Thread):
    '''
    Permite manipular a los meseros de una forma sencilla. Implementa un planificador para determinar que mesa
    es la que se va a atender primero.
    
    Atributos:
    mesas list(Mesa): Mesas que se estan usando
    meseros list(Mesero): Meseros que se encuentren en el servicio
    '''
    def __init__(self, cocina, numero_mesas, numero_meseros):
        Thread.__init__(self)
        self.cocina = cocina
        self.semaforo_mesas = Semaphore(numero_mesas)
        self.mesas = [Mesa(i) for i in range(numero_mesas)]
        self.meseros = [Mesero(i, self) for i in range(numero_meseros)]
        self.semaforo_meseros = Semaphore(0)
        self.mutex_comidas = Semaphore(1)
        self.comidas = []
        self.atencion = []
        self.mutex_atencion = Semaphore(1)
        self.mutex_lista_meseros = Semaphore(1)

    def run(self):
        for mesero in self.meseros:
            mesero.start()
        while True:
            self.semaforo_meseros.acquire()
            self.mutex_atencion.acquire()
            if self.atencion:
                mesa, estado = self.atencion.pop(0)
                mesero = self.obtener_mesero_disponible()
                mesero.estado = estado
                mesero.senalizador.release()
                mesero.mesa = mesa
                self.mutex_atencion.release()
            else:                
                self.mutex_atencion.release()
                self.mutex_comidas.acquire()
                if len(self.comidas) > 0:
                    orden = self.comidas[0]
                    mesero = self.obtener_mesero_disponible()
                    mesero.estado = EstadosMesero.llevar_comida
                    mesero.senalizador.release()
                    mesero.mesa = orden.mesa
                else:
                    self.semaforo_meseros.release()
                self.mutex_comidas.release()

    def dar_orden(self, orden):
        self.cocina.anadir_orden(orden)

    def anadir_orden_lista(self, orden):
        self.mutex_comidas.acquire()
        self.comidas.append(orden)
        self.mutex_comidas.release()

    def obtener_orden_cola(self):
        self.mutex_comidas.acquire()
        if self.comidas:
            self.comidas.pop(0)
        self.mutex_comidas.release()

    def obtener_mesero_disponible(self):  # Puede ser region critica
        self.mutex_lista_meseros.acquire()
        meserito = None
        for mesero in self.meseros:
            if mesero.esta_disponible():
                meserito =  mesero
                break
        meserito.estado = EstadosMesero.ocupado
        self.mutex_lista_meseros.release()
        return meserito

    def pedir_cuenta(self, mesa):
        self.mutex_atencion.acquire()
        self.atencion.append((mesa, EstadosMesero.atender_mesa))
        self.mutex_atencion.release()

    def tomar_orden(self, mesa):
        self.mutex_atencion.acquire()
        self.atencion.append((mesa, EstadosMesero.tomar_orden))
        self.mutex_atencion.release()

    def adquirir_mesa(self, grupo):
        self.semaforo_mesas.acquire()
        mesita = None
        for mesa in self.mesas:
            if mesa.esta_disponible():
                mesa.ocupar_mesa(grupo)
                mesita = mesa
                break 
        orden = Orden(mesita, self, grupo)
        self.semaforo_mesas.release()
        return orden

    