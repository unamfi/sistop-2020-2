"""
Modulo que contiene funciones utiles
"""

from threading import Thread
from abc import ABC, abstractmethod

def siguiente_estado(siguiente = None):
    def decorador(func):
        def salida(self, *arg, **args):
            func(self, *arg, **args)
            self.estado = siguiente
        salida.__name__ = func.__name__
        return salida
    return decorador

def estado_final(f):
    return None

class Persona(Thread, ABC):
    """
    Permite crear a entidades que usen el patron de diseño state de una forma mas sencilla
    """
    def __init__(self, id, Estados):
        Thread.__init__(self)
        self.id = id
        self.estado = Estados.inicial

    def run(self):
        while self.estado:
            self.estado(self, self)
       
    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '{}: {}'.format(self, self.estado.__name__)