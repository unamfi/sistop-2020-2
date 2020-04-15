"""
Permite manipular a los cocineros de una forma sencilla 
"""
from .comun import Persona
from enum import Enum, unique
from threading import Thread
from random import random, randint 
from time import sleep 

class Cocinero(Persona):
    """
    Representacion de un cocinero
    """
    def __init__(self,id):
        super.__init__(self,id,EstadosCocinero)

    def run(self):
        while self.estado:
            self.estado(self, self)
       
    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '{}: {}'.format(self, self.estado.__name__)
    
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
        pass

    def existe_activo(self):
        """
        Determina si existe aún algun cocinero libre
        """
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __len__(self):
        pass


class EstadosCocinero(Enum):

    @siguiente_estado(siguiente = recibir_orden)
    def esperar_orden(self,this, *arg, **args):
        # Mutex
        pass
    
    @siguiente_estado(siguiente = cocinar)
    def recibir_orden(self, this, *arg, **args):  # orden como parametro
        ##Plantear como pedire las ordenes
        
    @siguiente_estado(siguiente = dejar_plato)
    def cocinar(self, this, *arg, **args):
        print("Cocinando")
        sleep(random() * 6 + .3)  # Simula que esta cocinando
 
    @siguiente_estado(siguiente = esperar_orden)
    def dejar_plato(self,this, *arg, **args):
        #plato terminado, debemos regresarlo
    
    inicial = esperar_orden
    def __str__(self):
        return str(self.name)