"""
Contiene lógica que simula a un comensal y a grupos de los mismos
"""
from menu import platillos_azar, bebidas_azar, Orden
from comun import siguiente_estado, Persona, estado_final

from enum import Enum, unique
from threading import Thread, Semaphore
from random import random, randint 
from time import sleep

@unique
class EstadosComensal(Enum):

    @estado_final
    def salir(self, *arg, **args):
        pass

    @siguiente_estado(siguiente = salir)
    def levantarse(self, this, *arg, **args): 
        grupo = this.orden.grupo
        grupo.mutex_cuenta3.acquire()
        grupo.cuenta3 = grupo.cuenta3 + 1
        if grupo.cuenta3 == len(grupo):
            grupo.barrera_salir.release()
            grupo.senalador.release()  # Le avisamos que desocupe la mesa
        grupo.mutex_cuenta3.release()
        grupo.barrera_salir.acquire()
        grupo.barrera_salir.release()

    @siguiente_estado(siguiente = levantarse)
    def pagando(self, this, *arg, **args):
        grupo = this.orden.grupo
        grupo.esperar_mesero.acquiere()  # Esperar cuenta
        grupo.esperar_mesero.release()
        sleep(random() * 2 + .3)  # Simula sacar dinero
    
    @siguiente_estado(siguiente = pagando)
    def termino_comer(self, this, *arg, **args):
        grupo = this.orden.grupo
        grupo.mutex_cuenta2.acquire()
        grupo.cuenta2 = grupo.cuenta2 + 1
        if grupo.cuenta2 == len(grupo):
            grupo.barrera_terminar_comer.release()
            grupo.senalador.release()
        grupo.mutex_cuenta2.release()
        grupo.barrera_terminar_comer.acquire()
        grupo.barrera_terminar_comer.release()
        
        
    @siguiente_estado(siguiente = termino_comer)
    def comiendo(self, *arg, **args):
        sleep(random() * 2 + .3)  # Simula comer

    @siguiente_estado(siguiente = comiendo)
    def termino_orden(self, this, *arg, **args):
        grupo = this.orden.grupo
        grupo.mutex_cuenta.acquire()
        grupo.cuenta1 = grupo.cuenta + 1
        if grupo.cuenta1 == len(grupo):
            grupo.barrera_terminar_ordenar.release()
            grupo.dar_orden(this.orden) # Pasarlo a grupo
        grupo.mutex_cuenta.release()
        grupo.barrera_terminar_ordenar.acquire()
        grupo.barrera_terminar_ordenar.release()
        grupo.esperar_mesero.acquiere()  # Esperar comida
        grupo.esperar_mesero.release()

    @siguiente_estado(siguiente = termino_orden)
    def pidiendo_orden(self, this, *arg, **args):  
        bebidas = bebidas_azar(randint(1, 3))
        platillos = platillos_azar(randint(1, 4))
        grupo = this.orden.grupo
        grupo.esperar_mesero_atender.acquiere()  # Esperar mesero para atender, no hecho
        grupo.esperar_mesero_atender.release()
        this.orden.anadir_a_orden(bebidas)  # Region Critica
        this.orden.anadir_a_orden(platillos)  # Region Critica
        
    @siguiente_estado(siguiente = pidiendo_orden)
    def pensando_orden(self, *arg, **args):
        print("Pensando Orden")
        sleep(random() * 2 + .3)  # Simula pensar orden

    @siguiente_estado(siguiente = pensando_orden)
    def esperando_mesa(self, *arg, **args):
        print("Esperando Mesa")
    
    inicial = esperando_mesa

    def __str__(self):
        return str(self.name)

class Comensal(Persona):
    """
    Clase que representa a una persona que desea ir a comer al restaurante.
    Se activa el hilo una vez el individuo esta sentado en la mesa
    """
    def __init__(self, id):
        super().__init__(id, EstadosComensal)

    def recibir_orden(self, orden):
        self.orden = orden
    
class EstadosGrupo(Enum):

    @estado_final
    def final(self, this, *arg, **argv):
        pass

    @siguiente_estado(siguiente=final)
    def salir(self, this, *arg, **argv):
        this.mesa.desocupar_mesa()  # Desocupa la mesa

    @siguiente_estado(siguiente = salir)
    def pedir_cuenta(self, this, *arg, **argv):
        this.orden.servicio.pedir_cuenta(this.orden.mesa)
        this.senalador.acquire()  # El mesero lleva la cuenta
        this.esperar_mesero.release()  # Libera a los procesos para pagar
        print("Pidieron la cuenta en la mesa", this.orden.mesa)
        this.senalador.acquire()  # Espera a que todos hallan pagado
    
    @siguiente_estado(siguiente = pedir_cuenta)
    def esperar_todos_terminen_comer(self, this, *arg, **argv):
        this.senalador.acquire()  # Espera a que todos terminen de comer
        print("En la mesa", this.orden.mesa, "todos han terminado de comer")

    @siguiente_estado(siguiente = esperar_todos_terminen_comer)
    def esperar_comida(self, this, *arg, **argv):
        this.senalador.acquire()  # Espera a que traigan la comida
        this.esperar_mesero.release()  # Permite que todos coman

    @siguiente_estado(siguiente = esperar_comida)
    def esperar_mesero_pedir_orden(self, this, *arg, **argv):
        this.orden.servicio.tomar_orden(this.orden.mesa)
        this.senalador.acquire()  # Espera a que venga el mesero para pedir la orden
        this.esperar_mesero.release()  # Permite que todos pidan la orden

    @siguiente_estado(siguiente = esperar_mesero_pedir_orden)
    def sentar_comensales(self, this, *arg, **argv):
        print("El grupo de personas", this, "ha adquirido la mesa", this.orden.mesa)
        for comensal in this.comensales:
            comensal.asignar_orden(this.orden)
            comensal.start()

    @siguiente_estado(siguiente = sentar_comensales)
    def esperar_mesa(self, this, *arg, **argv):
        print("El grupo de personas", this, "se encuentra esperando una mesa")
        this.orden = this.servicio.adquirir_mesa(this)  

    inicial = esperar_mesa

    def __str__(self):
        return str(self.name)

class Grupo(Persona):
    """
    Clase que representa un grupo de personas que van juntos a un restaurante,
    un Grupo se compone de una persona o más.
    Esta clase es la encargada que el grupo espere la mesa y se vayan a sentar a una. 
    Una vez que las personas se salgan este hilo finaliza

    Atributos:
    comensales list(Comensal): Lista de comensales que representa un grupito de personas que fueron a comer juntos
    """
    def __init__(self, n, servicio):
        """
        Crea un grupo con n comensales
        """
        Thread.__init__(self)
        self.comensales = [Comensal(i + 1) for i in range(n)]
        self.servicio = servicio
        self.cuenta1 = self.cuenta2 = self.cuenta3 = 0
        self.mutex_cuenta1 = Semaphore(1)  # para barrera terminar ordenar
        self.mutex_cuenta2 = Semaphore(2)  # Para barrera terminar comer
        self.mutex_cuenta3 = Semaphore(3)  # Para barrera terminar salir
        self.barrera_terminar_ordenar = Semaphore(0)
        self.barrera_terminar_comer = Semaphore(0)
        self.barrera_salir = Semaphore(0)
        self.senalador = Semaphore(0)  # Indica pedir la cuenta al mesero
        self.esperar_mesero = Semaphore(0)

    def __str__(self):
        return '; '.join(map(str, self.comensales)) 

    def __repr__(self):
        return '; '.join(map(repr, self.comensales)) 

    def __len__(self):
        return len(self.comensales)

class Clientes:  
    """
    Clase que facilita la manipulacion de grupos de comensales

    Atributos:
    lista_grupos (list(Grupo)): Todos los grupos creados
    """
    def __init__(self, n, m, servicio):
        '''
        Permite crear n grupos con un máximo de m personas. Cada grupo puede tener diferente
        tamaño de personas
        '''
        self.grupos = [Grupo(randint(1, m), servicio) for i in range(randint(1, n))]
        

    def iniciar(self):
        for g in self.grupos:
            g.start()

    def existe_activo(self):
        """
        Determina si uno de los grupos todavia esta esperando mesa
        """
        return any(filter(lambda g : g.is_alive(), self.grupos))

    def __str__(self):
        return '\n'.join(map(str, self.grupos))

    def __repr__(self):
        return '{}\n{}'.format('\n'.join(map(repr, self.grupos)), len(self.grupos))

    def __len__(self):
        return len(self.grupos)

if __name__ == "__main__":
    a = Comensal(1)
    a.start()
    while a.is_alive():
        print(repr(a))
        sleep(.4)
