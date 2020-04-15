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

class EstadosMesero(Enum):

    def disponible(self, this, *arg, **argv):
        this.servicio.semaforo_meseros.release()
        this.senalizador.acquire()

    @siguiente_estado(siguiente = disponible)
    def tomar_orden(self, this, *arg, **argv):
        this.servicio.semaforo_meseros.acquire()
        this.mesa.grupo.senalador.release()  # Simula
        print("El mesero", this, "tomo la orden de la mesa", this.mesa)

    @siguiente_estado(siguiente = disponible)
    def atender_mesa(self, this, *arg, **argv):
        this.servicio.semaforo_meseros.acquire()
        this.mesa.grupo.senalador.release()  # Simula atender a una mesa
        print("El mesero", this, "atendio la mesa", this.mesa)

    
    @siguiente_estado(siguiente = disponible)
    def llevar_comida(self, this, *arg, **argv):
        this.servicio.semaforo_meseros.acquire()  # Simula llevar comida a la mesa
        this.servicio.obtener_orden_cola()  # Simula obtener la comida
        this.mesa.grupo.senalador.release()  # Simula llevar la comida
        print("El mesero", this, "llevo la comida a la mesa", this.mesa)

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

    def run(self):
        while True:
            self.semaforo_meseros.acquire()
            
    def dar_orden(self, orden):
        self.cocina.anadir_orden(orden)

    def anadir_orden_lista(self, orden):
        self.mutex_comidas.acquire()
        self.comidas.append(orden)
        self.mutex_comidas.release()

    def obtener_orden_cola(self):
        self.mutex_comidas.acquire()
        comida = self.comidas.pop(0)
        self.mutex_comidas.release()
        return comida

    def obtener_mesero_disponible(self):
        for mesero in self.meseros:
            if mesero.esta_disponible():
                return mesero

    def pedir_cuenta(self, mesa):
        mesero_disponible = self.obtener_mesero_disponible()
        mesero_disponible.siguiente_estado(EstadosMesero.tomar_orden)
    
    def tomar_orden(self, mesa):
        mesero_disponible = self.obtener_mesero_disponible()
        mesero_disponible.siguiente_estado(EstadosMesero.tomar_orden)

    def adquirir_mesa(self, grupo):
        self.semaforo_mesas.acquire()
        mesita = None
        for mesa in self.mesas:
            if mesa.esta_disponible():
                mesa.ocupar_mesa(grupo)
                mesita = mesa
                break 
        orden = Orden(mesita, self, grupo)
        return orden

    