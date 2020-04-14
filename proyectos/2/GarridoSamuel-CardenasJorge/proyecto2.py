import threading 
import sys
import random

parentescos = ['Papá','Mamá','Bebe','Niño','Niña','Adolescente','Joven','Abuelo','Abuela','Perro','Gato']

DiccionarioTareas = {1:['Ordenar la cama','Acomodar la mesa','Lavar el baño','Barrer','Trapear','Sacudir','Planchar'],2:['Lavar la ropa','Cocinar','Ordenar el librero','Lavar los trastes'],3:['Ordenar la bodega','Podar el jardín']}


mutexTarea = threading.Semaphore(1)
mutexFamDisponible = threading.Semaphore(1)
mutexFamiliar = threading.Semaphore(1)


familiarDisponible =[]
listaDeTareas =[]

tareas = threading.Semaphore(0)
personas = threading.Semaphore(0)

class Tarea:
    def __init__(self,numero,requeridosParaUnaTarea,nombreTarea):
        self.integrantes = []
        self.equipo = 0

        self.cuenta = 0
        self.mutex = threading.Semaphore(1)
        self.barrera = threading.Semaphore(0)

        self.identificarTarea()


    def identificarTarea(self):
        global personas, mutexTarea, listaDeTareas
        familiares.acquire()
        listaDeTareas.pop(0)
         
        mutexTarea.release()

        self.realizarse()

        familiares.release()

    def realizarse(numero,nombreTarea):
        global personas, familiarDisponible, mutexFamDisponible, cantidad_personas
        familiares.acquire()
        mutexFamDisponible.acquire()
        familiar = familiarDisponible.pop(0)
        mutexFamDisponible.release()
        familiar.entrarDisponible(self.nombreTarea)
        personas.release()

class Persona:
    def __init__(self,numero,parentesco):
        self.descanso = threading.Semaphore(0)
        self.entrarDisponible()
        
    def entrarDisponible(self):
        mutexFamiliar.acquire()
        familiarDisponible.append(self)
        mutexFamiliar.release()

    def Trabajar(self):
        global mutexTarea, familiarDisponible
        self.descanso.release()
        print("está trabajando")
        self.entrarDisponible()


class Casa:
    def __init__(self, cantidad_personas, tareasdelDia):
        global listaDeTareas, familiarDisponible 
        for x in range(cantidad_personas):
            threading.Thread(target = Persona, args=[x,parentescos[random.randrange(10)]]).start()
        
        for y in range(tareasdelDia):
            requeridosParalaTarea = random.randrange(1,3)
            posibilidad = DiccionarioTareas[requeridosParalaTarea]
            nombreTarea =random.choice(posibilidad)
            mutexTarea.acquire()          
            listaDeTareas.append(threading.Thread(target = Tarea, args= [y, requeridosParalaTarea,nombreTarea]).start())
            mutexTarea.release() 
     
cantidad_personas = 0
if __name__ == '__main__':
    global tareas, personas, cantidad_personas
    tareasdelDia = int(input("Ingrese el número de queaseres en la casa: "))
    cantidad_personas = int(input("Ingrese el número de familiares en la casa: "))
    tareas = threading.Semaphore(tareasdelDia)
    personas = threading.Semaphore(cantidad_personas)
    cuarentena = Casa(cantidad_personas,tareasdelDia)

