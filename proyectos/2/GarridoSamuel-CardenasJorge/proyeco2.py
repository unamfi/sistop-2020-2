import threading 
import sys
import random

parentescos = ['Papá','Mamá','Bebe','Niño','Niña','Adolescente','Joven','Abuelo','Abuela','Perro','Gato']

mutexTarea = threading.Semaphore(1)
mutexFamDisponible = threading.Semaphore(1)
mutexFamiliar = threading.Semaphore(1)

tarea = threading.Semaphore(numero_tareas)
familiares = threading.Semaphore(personas_en_casa)

familiarDisponible =[]
listaDeTareas =[]

class Persona:
    def __init__(self,numero,parentesco):
        self.descanso = threading.Semaphore(0)
        self.empezarDia()

    def empezarDia(self):
        global familiarDisponible
        mutexFamiliar.acquire()
        familiarDisponible.append(self)
        mutexFamiliar.release()

    def Trabajar(self,nombreTarea,numero,parentesco):
        global mutexTarea, familiarDisponible
        self.descanso.release()
        print(parentesco," ",numero," está ",nombreTarea)

class Casa:
	def __init__(self, cantidad_personas, tareasdelDia):
        global listaDeTareas, familiarDisponible
        
        for x in range(cantidad_personas):
            threading.Thread(target = Persona, args=[x,parentescos[random.randrange(10)]]).start()
        
        for y in range(self.tareasdelDia):
            requeridosParaUnaTarea = random.randrange(1,3)
            mutexTarea.acquire()          
            listaDeTareas.append(threading.Thread(target = Tarea, args= [y, requeridosParaUnaTarea]).start())
            mutexTarea.release() 
     

if __name__ == '__main__':
	tareasdelDia = int(intput("Ingrese el número de queaseres en la casa: "))
	cantidad_personas = int(intput("Ingrese el número de familiares en la casa: "))
    cuarentena = Casa(cantidad_personas,tareasdelDia)

## TORNIQUETE PARA ATENDER A LAS TAREAS. 

