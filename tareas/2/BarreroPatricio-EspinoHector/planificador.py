# Incluimos modulos necesarias
from random import randint
from string import ascii_uppercase
from functools import total_ordering
from abc import ABC, abstractmethod
from copy import deepcopy
from bisect import insort
from heapq import heappush, heappop

#Estos modulos requieren instalarse con pip
from scipy.stats import binom
from numpy.random import choice
import numpy as np

#Funcion que halla promedio de una lista
promedio = lambda v : sum(v) / len(v)

@total_ordering
class Proceso:
    """
    Clase que abstrae el concepto de un proceso
    """
    def __init__(self,  inicio, tiempo, letra):
        """
        Constructor de la clase
        -----
        int inicio -> tic el cual inicia
        int tiempo -> duración del proceso en tics
        str letra -> letra que identifica al proceso
        """
        self.inicio = inicio   
        self.tiempo = tiempo  
        self.letra = letra  
        self.tiempo_o = tiempo  
        self.get_atr = letra  
    
    def letra_tiempo(self):
        """
        Regresa la letra y la duracion del proceso
        --- returns
        str letra -> letra del proceso
        int tiempo -> duracion del proceso
        """
        return self.letra, self.tiempo
    
    def ejecutar(self, tiempo_a_ejecutar):
        """
        Ejecuta un proceso
        ---- params
        int tiempo_a_ejecutar: Tiempo que se va a ejecutar el proceso
        """
        self.tiempo -= tiempo_a_ejecutar
        #sleep va a ir aqui, debe estar en funcion de tiempo_a_ejecutar

    def esta_activo(self):
        '''
        Determina si el proceso esta activo (aun le falta por ejecutarse)
        --- returns
        bool El proceso esta listo?
        '''
        return self.tiempo > 0

    def puede_ejecutar(self, t):
        '''
        Determina si el proceso puede ser ejecutado
        --- returns
        bool -> El proceso se puede ejecutar?
        '''
        return self.esta_activo() and self.inicio <= t
    
    def __repr__(self):
        '''
        Muestra informacion detallada sobre el proceso
        ---- returns
        str -> descripcion del proceso
        '''
        return "{}: {}, t={}".format(self.letra, self.inicio, self.tiempo)
    
    def __str__(self):
        '''
        Muestra informacion sobre el proceso
        ---- returns
        str -> descripcion del proceso
        '''
        return self.letra

    def __eq__(self, other):
        '''
        Determina la igualdad de dos procesos
        ---- params
        Proceso other -> proceso con el cual queremos compararlo
        ---- returns
        bool -> Si dos procesos son iguales
        ---- raise
        TypeError -> Error en los tipos de datos de las comparaciones
        '''
        if type(other) != Proceso:
            raise TypeError("No se puede comparar {} con Proceso".format(type(other)))
        if type(self.get_atr) != type(other.get_atr):
            raise TypeError("No se puede comparar {}: {} con {}: {} ".format(
                type(self.get_atr),self.get_atr,type(other.get_atr),other.get_atr))
        return self.get_atr == other.get_atr
      
    def __lt__(self, other):
        '''
        Determina si el proceso actual es menor que other
        ---- params
        Proceso other -> proceso con el cual queremos compararlo
        ---- returns
        bool -> Si dos procesos son iguales
        ---- raise
        TypeError -> Error en los tipos de datos de las comparaciones
        '''
        if type(other) != Proceso:
            raise TypeError("No se puede comparar {} con Proceso".format(type(other)))
        if type(self.get_atr) != type(other.get_atr):
            raise TypeError("No se puede comparar {}: {} con {}: {} ".format(
                type(self.get_atr),self.get_atr,type(other.get_atr),other.get_atr))
        return self.get_atr < other.get_atr    

    def __hash__(self):
        '''
        Obtiene la hash del proceso
        --- returns
        int -> hash del proceso
        '''
        return hash(self.get_atr)

    def __add__(self, other):
        '''
        Realiza la suma de dos procesos
        ---- params
        Proceso other -> proceso con el cual queremos sumarlo
        ---- returns
        Proceso -> Suma de los procesos
        ---- raise
        TypeError -> Error en los tipos de datos de las comparaciones
        '''
        if type(other) != Proceso:
            raise TypeError("No se puede comparar {} con Proceso".format(type(other)))
        return Proceso(self.inicio+other.inicio,
                      self.tiempo + other.tiempo, 
                      self.letra+other.letra)

    def __int__(self):
        return self.tiempo

Proceso.nulo = Proceso(0, 0, '')

class Manipulador:
    '''
    Clase que permite manipular procesos de forma sencilla
    '''
    def generar_procesos_aleatorios(self, num_procesos, tiempo_total):
        '''
        Permite crear procesos aleatorios
        ---- params
        int num_procesos -> Numero de procesos que se desea
        int tiempo_total -> Suma de todas las duraciones de los procesos 
        '''
        n = int(4.05 * tiempo_total)
        p = 1 / 9
        tiempos_iniciales = np.sort(binom.rvs(n, p, size = num_procesos)) ##cuando inicia un proceso
        media = tiempo_total//num_procesos
        var = media // 2
        tiempo = tiempo_total - tiempo_total//num_procesos * num_procesos 
        varianzas = []
        for i in range(num_procesos - 1):
            ran = randint(-var, var)
            tiempo -= ran
            varianzas.append(ran)
        varianzas.append(tiempo)
        tiempos = np.repeat(media, num_procesos) + \
                np.array(varianzas[::-1]) ##Cuanto dura el proceso
        if tiempos[0] <= 0:
            n = abs(tiempos[0]) + 1
            n = n + media % n
            tiempos = tiempos + n 
        self.procesos_original = [Proceso(i, t, l) for i, t, l in zip(tiempos_iniciales,
                                                            tiempos, ascii_uppercase)]
        self.tiempo_total_original = tiempo_total

    def __init__(self, num_procesos, tiempo_total, procesos = None):
        """
        Permite crear varios procesos aleatorios
        params:
            int num_procesos => numero de procesos requeridos, debe ser mayor a uno
            int tiempo_total => tiempo total que tardan todos los procesos
                                recomendable que sea divisible entre 5
        """
        if not procesos:
            self.generar_procesos_aleatorios(num_procesos, tiempo_total)
        else:
            self.procesos_original = deepcopy(procesos)
            self.tiempo_total_original = tiempo_total
        self.reiniciar()

    def reiniciar(self):
        '''
        Establece a condiciones iniciales el manipulador
        '''
        self.procesos = deepcopy(self.procesos_original)
        self.num_procesos = len(self.procesos)
        self.tiempo_total = self.tiempo_total_original
        self.procesos_mandados = set()
        self.t = 0 
        self.T = []
        self.E = []
        self.P = []

    def existen_activos(self):
        '''
        Determina si existen procesos activos
        --- returns
        bool -> si es existen procesos activos
        '''
        return any(list(filter(lambda p : p.esta_activo(), self.procesos)))
    
    def procesos_a_ejecutar(self):  # Lista de procesos
        '''
        Regresa los procesos para ejecutar
        --- returns
        list Proceso -> lista de procesos que van a ejecutar
        '''
        todos = set(filter(lambda p : p.puede_ejecutar(self.t), self.procesos))
        ret = sorted(list(todos - self.procesos_mandados))
        self.procesos_mandados = todos
        return ret

    def obtener_proceso(self, letra, t):
        '''
        Obtiene el proceso mediante una determinada letra, e incrementa los tics acutales
        --- params
        str letra -> letra del proceso a buscar
        int t -> numero de tics que se desea incrementar
        --- returns
        Proceso -> proceso buscado
        '''
        self.t = self.t + t
        self.tiempo_total -= t
        for i, p in enumerate(self.procesos):
            if p.letra == letra:
                return self.procesos[i]

    def agregar_proceso_concluido(self, proceso):
        '''
        Permite almacenar un proceso concluido para obtener las metricas T, E, P
        '''
        T = self.t - proceso.inicio
        E = T - proceso.tiempo_o
        P = T / proceso.tiempo_o
        self.T.append(T)
        self.E.append(E)
        self.P.append(P)

    def resultados(self):
        '''
        Regresa las metricas T, E, P
        '''
        return promedio(self.T), promedio(self.E), promedio(self.P)
    
    def __str__(self):
        '''
        Muestra información del manipulador
        --- returns
        str -> Informacion del manipulador
        '''
        return ''.join([repr(p)+'; ' for p in self.procesos])[:-1] + " " + \
               '(tot:' + str(self.tiempo_total) + ')'
  
class Planificador(ABC):
    '''
    Clase abstracta que abstrae el concepto de un planificador
    '''
    @abstractmethod
    def posee_procesos(self):
        pass
  
    def siguiente_proceso(self, procesos_a_ejecutar):  #  Puede recibir una lista vacia y no hay dentro en ese caso regresar '*', 0
        '''
        Obtiene el siguiente proceso a ejecutar junto con su tiempo
        --- params 
        list Proceso procesos_a_ejecutar -> Lista de procesos nuevos que se desean ejecutar
        --- returns
        str, int -> str: letra del proceso a ejecutar, int: cuanto tiempo se ejecutara ese proceso
        '''        
        if not self.posee_procesos() and not procesos_a_ejecutar: # Regresa letra del proceso, tiempo que se va a ejecutar.
            return '*', 1 

class FCFS(Planificador):
    def __init__(self):
        self.cola = []

    def posee_procesos(self):
        return self.cola

    def siguiente_proceso(self, procesos_a_ejecutar):
        c = super().siguiente_proceso(procesos_a_ejecutar)
        if c: return c
        self.cola.extend(procesos_a_ejecutar)
        return self.cola.pop(0).letra_tiempo()

class SPN(Planificador):
    
    def __init__(self):
        self.lista = []

    def posee_procesos(self):
        return self.lista 
    
    def siguiente_proceso(self, procesos_a_ejecutar):
        c = super().siguiente_proceso(procesos_a_ejecutar)
        if c: return c
        for p in procesos_a_ejecutar:
            p = deepcopy(p)
            p.get_atr = p.tiempo
            insort(self.lista, p)
        return self.lista.pop(0).letra_tiempo()



class FB(Planificador):
    
    def __init__(self, f):  # La duracion del cuantum es una funcion f, que recibe el nivel donde se encuntra el proceso
        self.heap = []
        self.calcular_tiempo = lambda n, p : min(f(n), p.tiempo)

    def posee_procesos(self):
        return self.heap

    def limpiar_lista(self):
        self.heap = list(filter(lambda p : p[1].esta_activo(), self.heap))

    def siguiente_proceso(self, procesos_a_ejecutar):
        self.limpiar_lista()
        c = super().siguiente_proceso(procesos_a_ejecutar)
        if c: return c
        for p in procesos_a_ejecutar:
            heappush(self.heap, (0, p))
        nivel, p = heappop(self.heap)
        tiempo = self.calcular_tiempo(nivel, p)
        heappush(self.heap, (nivel+1, p))
        return p.letra, tiempo

class RR(Planificador):
    def __init__(self,pato):# pato = quantum
        self.cola = []
        self.pato=pato
        self.anterior = None
    
    def reposicionar(self):
        if self.anterior:
            self.cola.append(self.anterior)
        else:
            print("No hay anterior, algo salio mal")

    def posee_procesos(self):
        return self.cola

    def siguiente_proceso(self, procesos_a_ejecutar):
        c = super().siguiente_proceso(procesos_a_ejecutar)
        self.cola.extend(procesos_a_ejecutar)
        if c and not self.anterior:
            return c
        elif self.anterior:
            self.reposicionar()

        self.anterior = self.cola.pop(0)
        tiempo = self.pato
        letra = self.anterior.letra
        if self.anterior.tiempo <= tiempo:
            tiempo = self.anterior.tiempo
            self.anterior = None
        return letra,tiempo

class SRR(RR):
    def __init__(self,pato,a,b):###a = nuevos , b =aceptados
        super().__init__(pato)
        self.a = a
        self.b=b
        self.top_new = 0
        self.top_acc = 0
        self.new = []
        ###cola == self.acc

    def siguiente_proceso(self,procesos_a_ejecutar):
        to_add = []
        if procesos_a_ejecutar:
            self.new.extend([[x,0] for x in procesos_a_ejecutar]) ## new[proceso,valor_new]
        if self.top_acc<=self.top_new or  (not self.cola and not self.anterior):
            if not self.cola and not self.anterior:
                self.top_acc=self.top_new
            to_add = [ i[0] for i in filter(lambda x: x[1]>=self.top_acc,self.new)] ##Se agregan solo aquellos que cumplan con uno de los dos criterios
            self.new = list(filter(lambda x: x[1]<self.top_acc,self.new))
        letra,tiempo = RR.siguiente_proceso(self,to_add)###ejecutamos la RR
        if self.new:
            self.new = [ [x,y+self.a] for x,y in self.new] ### sumamos al de new
            self.top_new = self.new[0][1]
        else:
            self.top_new = 0
        self.top_acc+=self.b
        return letra,tiempo

def probar_planificador(Planificador, procesos): 
    '''
    Permite poner a prueba un planificador con determinados procesos
    ---
    callable Planificador -> Callable que regresa una instancia de un Planificador
    Manipulador procesos -> Conjunto de procesos con el que se quiere probar al Planificador 
    '''
    planificador = Planificador()
    while procesos.existen_activos():
        procesos_a_ejecutar = procesos.procesos_a_ejecutar()
        
        letra, tiempo_a_ejecutar = planificador.siguiente_proceso(procesos_a_ejecutar)
        
        print(letra * tiempo_a_ejecutar, end='')
        proceso = procesos.obtener_proceso(letra, tiempo_a_ejecutar)

        if proceso:
            proceso.ejecutar(tiempo_a_ejecutar)
            if not proceso.esta_activo():
                procesos.agregar_proceso_concluido(proceso)
    return procesos.resultados()

#PROBANDO CASOS ALEATORIOS

#Constantes de pruebas random
numero_rondas = 5
num_procesos = 6

#Definiciones de planificadores especificos
def RR_4(): return RR(4)
def RR_1(): return RR(1)
def FB_exponencial(): return FB(lambda n : 2 ** n)
def FB_constante_1(): return FB(lambda n : 1)
def FB_lineal(): return FB(lambda n : n)
def SRR_q_5_a_2_b_1(): return SRR(4,2,1)
planificadores = [FCFS, RR_1, RR_4, SPN, SRR_q_5_a_2_b_1, FB_exponencial, FB_constante_1, FB_lineal]

#Pruebas aleatorias
for ronda in range(numero_rondas):
    tiempo_total = randint(18, 25)
    print("---Ronda #{}---".format(ronda+1))
    procesos = Manipulador(num_procesos, tiempo_total)
    print(procesos)
    for Plan in planificadores:
        print('**{}**'.format(Plan.__name__.upper()))
        procesos.reiniciar()
        datos = probar_planificador(Plan, procesos)
        print('\nDatos: T={}, E={}, P={}'.format(*datos))
    print("\n")


# Pruebas de Ejemplos de Gunnar
print("----Caso Gunnar---")
A = Proceso(0, 3, 'A')
B = Proceso(1, 5, 'B')
C = Proceso(3, 2, 'C')
D = Proceso(9, 5, 'D')
E = Proceso(12, 5, 'E')
lista_procesos = [A,B,C,D,E]
procesos = Manipulador(len(lista_procesos), 
                       int(sum(lista_procesos, Proceso.nulo)), 
                       lista_procesos)
print(procesos)
for Plan in planificadores:
    print('**{}**'.format(Plan.__name__.upper()))
    procesos.reiniciar()
    datos = probar_planificador(Plan, procesos)
    print('\nDatos: T={}, E={}, P={}'.format(*datos))


