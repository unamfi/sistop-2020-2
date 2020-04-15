import threading 
import sys
import random
import time


parentescos = ['Papá','Mamá','Bebe','Niño','Niña','Adolescente','Joven','Abuelo','Abuela','Perro','Gato']
DiccionarioTareas = {1:['Ordenar la cama','Acomodar la mesa','Lavar el baño','Barrer','Trapear','Sacudir','Planchar'],2:['Lavar la ropa','Cocinar','Ordenar el librero','Lavar los trastes'],3:['Ordenar la bodega','Podar el jardín']}
mutexTarea = threading.Semaphore(1)
mutexFamiliar = threading.Semaphore(1)
familiarDisponible =[]
listaDeTareas =[]
cantidad_personas = 20
tareasdelDia = 20   
tareas = threading.Semaphore(tareasdelDia)
personas = threading.Semaphore(cantidad_personas)

class Tarea:
    def __init__(self,numero,requeridosParaUnaTarea,nombreTarea):
        self.numero = numero
        self.requeridosParaUnaTarea = requeridosParaUnaTarea
        self.nombreTarea = nombreTarea
        self.mutex = threading.Semaphore(1)
        self.barrera = threading.Semaphore(0)
        self.identificarTarea()


    def identificarTarea(self):
        global personas, mutexTarea, listaDeTareas
        mutexTarea.acquire()
        listaDeTareas.pop(0)
        self.realizarse(self.numero,self.nombreTarea,self.requeridosParaUnaTarea)
        mutexTarea.release()

    def realizarse(self,numero,nombreTarea,requeridosParalaTarea):
        global personas, familiarDisponible, cantidad_personas
        requeridos = []
        for i in range(requeridosParalaTarea):
            personas.acquire()
            mutexFamiliar.acquire()
            requeridos.append(familiarDisponible.pop(random.randrange(len(familiarDisponible))))
            mutexFamiliar.release()
        for i in requeridos:
            i.Trabajar(nombreTarea)
        while True:
            if all(elem in familiarDisponible for elem in requeridos):
                print('\n\t',requeridosParalaTarea,'ha(n) terminado la tarea:',nombreTarea,'\n')
                self.barrera.release()
                break
        for i in range(requeridosParalaTarea):
            personas.release()

class Persona:
    def __init__(self,numero,parentesco):
        self.numero = numero
        self.parentesco = parentesco
        self.descanso = threading.Semaphore(0)
        self.entrarDisponible('vacio')

    def entrarDisponible(self,nombreTarea):
        if nombreTarea == 'vacio':
            mutexFamiliar.acquire()
            print(self.parentesco,self.numero,'está listo para el trabajo')
            familiarDisponible.append(self)
            mutexFamiliar.release()
        else:
            mutexFamiliar.acquire()
            familiarDisponible.append(self)
            mutexFamiliar.release()

    def Trabajar(self,nombreTarea):
        global mutexTarea, familiarDisponible
        self.descanso.release()
        print(self.parentesco,self.numero,"está trabajando en",nombreTarea)
        time.sleep(random.random())
        print(self.parentesco,self.numero,'dejó de trabajar en',nombreTarea)
        self.entrarDisponible(nombreTarea)


class Casa:
    def __init__(self, cantidad_personas, tareasdelDia):
        global listaDeTareas, familiarDisponible 
        for x in range(cantidad_personas):
            threading.Thread(target = Persona, args=[x,parentescos[random.randrange(10)]]).start()
        
        for y in range(tareasdelDia):
            requeridosParalaTarea = random.randrange(1,4)
            posibilidad = DiccionarioTareas[requeridosParalaTarea]
            nombreTarea = random.choice(posibilidad)
            mutexTarea.acquire()          
            listaDeTareas.append(threading.Thread(target = Tarea, args= [y, requeridosParalaTarea,nombreTarea]).start())
            mutexTarea.release() 


if __name__ == '__main__':
    cuarentena = Casa(cantidad_personas,tareasdelDia)


