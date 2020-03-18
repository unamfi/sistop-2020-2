
from random import shuffle, random
from time import sleep  # recibe segundos
from threading import Semaphore, Thread

m = 5 # num_platos
k = 6 # num_gatos
l = 7 # num_raton

platos = Semaphore(m)
num_platos_activos = 0
mutex_platos = Semaphore(1)

def aumentar_platos_activos():
    global num_platos_activos
    mutex_platos.acquire()
    num_platos_activos += 1
    mutex_platos.release()

def disminuir_platos_activos():
    global num_platos_activos

    mutex_platos.acquire()
    num_platos_activos -= 1
    mutex_platos.release()

def leer_platos_activos():
    global num_platos_activos
    mutex_platos.acquire()
    num = num_platos_activos
    mutex_platos.release()
    return num

class Animal(Thread):
    def __init__(self, nombre):
        Thread.__init__(self)
        self.nombre = nombre
        self.mesa_lock = Semaphore(0)  # Señalizador
        self.plato = None
        
    def establecer_plato(self, plato):
        self.plato = plato

    def run(self):
        while True:
            print(self, "estoy esperando")
            self.mesa_lock.acquire() ##mimiendo, Señalizador
            self.plato.ocupar()
            print(self, "estoy comiendo en el plato", self.plato)
            sleep(6)
            self.plato.desocupar()
            platos.release()
            disminuir_platos_activos()
            print(self, "desocupe el plato", self.plato)
            lista_de_espera.append(self)

    def __str__(self):
        return self.nombre

class Gato(Animal):
    def __init__(self,nombre):
        Animal.__init__(self, nombre)

class Raton(Animal):
    def __init__(self,nombre):
        Animal.__init__(self, nombre)

lista_de_espera = [Gato("Gato "+str(i)) for i in range(k)]
lista_de_espera.extend([Raton("Raton "+str(i)) for i in range(l)])
shuffle(lista_de_espera)

class Plato: ##mutex
    def __init__(self, nombre):
        self.mutex = Semaphore(1)
        self.nombre = nombre
        self.esta_disponible = True

    def disponible(self):
        return self.esta_disponible

    def ocupar(self):
        self.mutex.acquire()
        self.esta_disponible = False

    def desocupar(self):
        self.esta_disponible = True
        self.mutex.release()

    def __str__(self):
        if self.disponible():
            estate = "libre"     
        else:
            estate = "ocupado"
        return "Plato #{} esta {}".format(self.nombre,estate)  

class Mesa:##Barrera
    def __init__(self):
        self.platos = [Plato(i) for i in range(m)]
        self.tipo = None

    def plato_disponible(self):
        for i, plato in enumerate(self.platos):
            if plato.disponible():
                return self.platos[i]

    def para_agregar(self):
        l = []
        for i, animal in enumerate(lista_de_espera):
            if type(animal) == self.tipo:
                l.append(lista_de_espera[i])
        return l

    def anadir_animal(self, animal):
        if self.tipo == None or self.tipo == type(animal):
            platos.acquire()  
            aumentar_platos_activos()
            animal.establecer_plato(self.plato_disponible())
            animal.mesa_lock.release()
            self.tipo = type(animal)
        else:  
            a_agregar = self.para_agregar()
            minimo = min(m - leer_platos_activos(), len(a_agregar))
            for i in range(minimo):
                animal = a_agregar[i]
                platos.acquire()  
                aumentar_platos_activos()
                animal.plato = self.plato_disponible()
                animal.mesa_lock.release()
            self.tipo = type(animal)
            self.anadir_animal(animal)
for animal in lista_de_espera:
    animal.start()

mesa = Mesa()
while lista_de_espera:
    animal = lista_de_espera.pop(0)
    mesa.anadir_animal(animal)