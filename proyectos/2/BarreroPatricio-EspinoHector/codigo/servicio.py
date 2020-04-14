"""
Contiene clases necesarias para facilitar el trabajo con servicio
"""

from threading import Thread

class Mesa:
    """
    Representa el concepto de una mesa     
    
    Atributos:        
    disponibilidad (int): tiene valores verdadero o falso indicando si la mesa esta disponible o no.  
    numero_mesa (int): El numero de la mesa
    
    """
    pass

class Mesero(Thread):
    
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

