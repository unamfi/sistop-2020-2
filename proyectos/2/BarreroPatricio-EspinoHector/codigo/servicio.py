"""
Contiene clases necesarias para facilitar el trabajo con servicio
"""

from threading import Thread, Semaphore

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

    def desocupar_mesa(self):
        self.mutex_mesa.acquire()
        self.disponibilidad = True
        self.mutex_mesa.release()

    def ocupar_mesa(self):
        self.mutex_mesa.acquire()
        self.disponibilidad = False
        self.mutex_mesa.release()

    def ver_disponibilidad(self):
        self.mutex_mesa.acquire()
        disponibilidad = self.disponibilidad
        self.mutex_mesa.release()
        return disponibilidad

class Mesero(Thread):
    def __init__(self):
        pass
        
class Servicio:
    '''
    Permite manipular a los meseros de una forma sencilla. Implementa un planificador para determinar que mesa
    es la que se va a atender primero.
    
    Atributos:
    mesas list(Mesa): Mesas que se estan usando
    meseros list(Mesero): Meseros que se encuentren en el servicio
    '''
    pass

