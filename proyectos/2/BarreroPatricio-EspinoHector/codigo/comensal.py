"""
Contiene lógica que simula a un comensal y a grupos de los mismos
"""

from threading import Thread

class Comensal(Thread):
    """
    Clase que representa a una persona que desea ir a comer al restaurante.
    Se activa el hilo una vez el individuo esta sentado en la mesa
    """
    pass

class Grupo(Thread):
    """
    Clase que representa un grupo de personas que van juntos a un restaurante,
    un Grupo se compone de una persona o más.
    Esta clase es la encargada que el grupo espere la mesa y se vayan a sentar a una. 
    Una vez que las personas se sienten este hilo finaliza
    """
    pass

class Clientes:  #is_alive()
    """
    Clase que facilita la manipulacion de grupos de comensales

    Atributos:
    lista_grupos (list(Grupo)): Todos los grupos creados
    """
    def __init__(self, n, m):
        '''
        Permite crear n grupos con un máximo de m personas. Cada grupo puede tener diferente
        tamaño de personas
        '''
        pass

    def existe_activo(self):
        """
        Determina si uno de los grupos todavia esta esperando mesa
        """
        pass

    def __str__(self):
        pass