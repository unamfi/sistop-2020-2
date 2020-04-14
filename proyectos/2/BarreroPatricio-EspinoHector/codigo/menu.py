"""
Contiene lógica para facilitar el uso de items de comida y ordenes
"""

from enum import Enum, unique
from copy import deepcopy

@unique
class Item(Enum):
    """
    Enumeración que representa tener items de un menú
    """
    Coca_Cola = 50, 'Bebida', 10

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, precio, categoria, tiempo):
        self.precio = precio
        self.categoria = categoria
        self.tiempo = tiempo  # Tiempo de preparacion
        
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
    def __init__(self, mesa_asociada, lista_item_cantidad, mesero):
        self.lista_original = deepcopy(lista_item_cantidad)
        self.mesa_asociada = mesa_asociada
        self.lista_item_cantidad = lista_item_cantidad
        self.mesero = mesero

    def siguente_item(self):
        return self.lista_item_cantidad.pop(0)

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
    '''
    pass

def bebidas_azar(n):
    '''
    Permite obtener n bebidas al azar

    parameters:
    n (int): cantidad de bebidas que se deseen 

    Returns:
    list(Item): n bebidas seleccionados al azar
    '''
    pass


if __name__ == "__main__":
    print(repr(Item.Coca_Cola))
    print(Item.Coca_Cola)