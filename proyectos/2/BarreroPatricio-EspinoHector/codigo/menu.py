"""
Contiene lógica para facilitar el uso de items de comida y ordenes
"""

from enum import Enum, unique
from copy import deepcopy
from random import sample

@unique
class Item(Enum):
    """
    Enumeración que representa tener items de un menú
    """
    Coca_Cola = 40, 'Bebida', 10
    Carne_Res = 140, 'Carnes', 60 * 20

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, precio, categoria, tiempo):
        self.precio = precio
        self.categoria = categoria
        self.tiempo = tiempo  # Tiempo de preparacion

    def es_bebida(self):
        return self.categoria.lower() == 'bebida'
        
    def __str__(self):
        return str(self.name).replace('_', ' ')

    def __int__(self):
        return self.precio

    def __repr__(self):
        return '{}-{}  cuesta:${}  tarda: {}[s]'.format(self, self.categoria, self.precio, self.tiempo)


class Orden:
    """
    Clase que representa la orden de una mesa
    """
    def __init__(self, mesa_asociada, mesero, grupo_personas):
        self.mesa_asociada = mesa_asociada
        self.lista_item_cantidad = dict()
        self.mesero = mesero
        self.grupo_personas = grupo_personas

    def siguente_item(self):
        return self.lista_item_cantidad.pop(0)

    def anadir_a_orden(self, items):  # Region critica, hiper critica jajaj
        for item in items:
            if item in self.lista_item_cantidad:
                self.lista_item_cantidad[item] = self.lista_item_cantidad[item] + 1
            else:
                self.lista_item_cantidad[item] = 1

    def orden_finalizada(self):
        self.lista_original = deepcopy(self.lista_item_cantidad)
        return self

    def __str__(self):
        return 'Orden de la mesa {}\n{}'.format(self.mesa_asociada, 
                '\n'.join([str(i) + '  x' + c for i, c in self.lista_original]))

def platillos_azar(n):
    '''
    Permite obtener n platillos al azar

    parameters:
    n (int): cantidad de platillos que se deseen 

    Returns:
    list(Item): n platillos seleccionados al azar

    Raises:
    ValueError: si n > todos los platillos
    '''
    return sample(list(filter(lambda item : not item.es_bebida(), list(Item))), k = n)

def bebidas_azar(n):
    '''
    Permite obtener n bebidas al azar

    parameters:
    n (int): cantidad de bebidas que se deseen 

    Returns:
    list(Item): n bebidas seleccionados al azar

    Raises:
    ValueError: si n > todas las bebidas
    '''
    return sample(list(filter(lambda item : item.es_bebida(), list(Item))), k = n)


if __name__ == "__main__":
    print(repr(Item.Coca_Cola))
    print(Item.Coca_Cola)
    print(list(Item))
    print(len(Item))
    print(bebidas_azar(2))