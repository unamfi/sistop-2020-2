from random import randrange
from threading import currentThread
from time import sleep

from modulos.agencia import agencia


class cliente(object):
    def __init__(self, Agencias: [agencia]):
        self.agencias = Agencias
        self.agenciaElegida = self.agencias[randrange(0,self.agencias.__len__())]


    def run(self):
        self.comprar(self.agenciaElegida)


    def comprar(self, ag : agencia):
        try:
            buscarAsiento = ag.getList()
            eleccion = buscarAsiento[buscarAsiento.index(min(buscarAsiento, key=lambda t: t[2]))]
            
            if (ag.vender_Cliente(eleccion[0], eleccion[1])):
                # viaje
                sleep(10)
                return eleccion
            else:
                sleep(0.1)
                self.comprar(ag)
        except:
            sleep(0.5)
            print('\n\nEl cliente ', str(currentThread().getName()),'no encontro vuelos') # en caso de que haya mas clientes que asientos.