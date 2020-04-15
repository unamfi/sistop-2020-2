## Creado por: Garrido Sánchez Samuel Arturo y Cárdenas Cárdenas Jorge
## 14 de Abril del 2020
## Sistemas Operativos, Proyecto 2


import threading 
import sys
import random
import time

## Lista de parentescos y diccionario que nos permite identificar 
parentescos = ['👨 Papá','👩‍🦱 Mamá','👶 Bebe','👦 Niño','👧 Niña','👱‍♀️ Adolescente','🧑 Joven','👴 Abuelo','👵 Abuela','🐕 Perro','🐈 Gato']
DiccionarioTareas = {1:['Ordenar la cama 🛌','Acomodar la mesa 🍴','Lavar el baño 🚽','Barrer 🧹','Trapear 🧹','Sacudir 💨','Planchar 👕'],2:['Lavar la ropa 🧼','Cocinar 🥘','Ordenar el librero 📚','Lavar los trastes 🍽'],3:['Ordenar la bodega 🗄','Podar el jardín 🌳']}

##Mutex para tenerlos en las clases tarea, persona y Casa
mutexTarea = threading.Semaphore(1)
mutexFamiliarT = threading.Semaphore(0)
mutexFamiliar = threading.Semaphore(1)
familiarDisponible =[]
listaDeTareas =[]

#Este número de personas se cambia cuando el usuario lo registra
cantidad_personas = 5
tareasdelDia = 5

## Multiplex evitar que se usen más personsa o tareas de los establecidos 
tareas = threading.Semaphore(tareasdelDia)
personas = threading.Semaphore(cantidad_personas)

#CeutnaListos para la barrera
cuentaListos = 0

#Mutex para la barrera y mutex de coronaviroso
mutexListos = threading.Semaphore(1)
barreraListos = threading.Semaphore(0)
coronaviroso = threading.Semaphore(1)

class Tarea:
    def __init__(self,numero,requeridosParaUnaTarea,nombreTarea):
        self.numero = numero
        self.requeridosParaUnaTarea = requeridosParaUnaTarea
        self.nombreTarea = nombreTarea
        self.barrera = threading.Semaphore(0)
        self.identificarTarea()


    def identificarTarea(self):
        global personas, mutexTarea, listaDeTareas
        mutexTarea.acquire()
        if cuentaListos == cantidad_personas:
                barreraListos.release()

        ##Detalle: Se quería inicialmente sacar todas las tareas a la vez, tal vez tener una tercera clase
        listaDeTareas.pop(0)
        self.realizarse(self.numero,self.nombreTarea,self.requeridosParaUnaTarea)
        #Sacamos una por una las tareas en el orden en que llegaron a listaDeTareas.append(threading.Thread(target = Tarea, args= [y, requeridosParalaTarea,nombreTarea]).start())
        mutexTarea.release()

    def realizarse(self,numero,nombreTarea,requeridosParalaTarea):
        global personas, familiarDisponible, cantidad_personas
        requeridos = []
        for i in range(requeridosParalaTarea):
            personas.acquire()
            mutexFamiliar.acquire()## Sacamos algunos de los familiares requeridos que estén disponibles para hacer la tarea
            requeridos.append(familiarDisponible.pop(random.randrange(len(familiarDisponible))))
            mutexFamiliar.release()
            mutexFamiliar.acquire()
            mutexFamiliar.release()
        for i in requeridos: ## A éstos los ponemos a trabajar
            i.Trabajar(nombreTarea)
        while True:
            if all(elem in familiarDisponible for elem in requeridos): ##Hasta que todos hayan terminado la tarea, se dará por concluída la tarea y quitamos la barrera
                print('\n\t',requeridosParalaTarea,'ha(n) terminado la tarea:',nombreTarea,'\n')
                self.barrera.release()
                self.barrera.acquire()
                self.barrera.release()
                break
        for i in range(requeridosParalaTarea): ##Liberamos los mutex para evitar que se usen más de las personas necesarias
            personas.release()

class Persona:
    def __init__(self,numero,parentesco):
        self.numero = numero 
        self.parentesco = parentesco
        self.descanso = threading.Semaphore(0)
        self.entrarDisponible('vacio')

    def entrarDisponible(self,nombreTarea):
        global cuentaListos,barreraListos,mutexListos
        if nombreTarea == 'vacio': ## la primera vez lo cachamos para v
            mutexFamiliar.acquire()

            cuentaListos = cuentaListos + 1
            print_pass(str(self.parentesco)+str(self.numero)+' está listo para el trabajo')
            mutexFamiliar.release()
            mutexFamiliar.acquire()# Para que pase uno por uno
            mutexFamiliar.release()
            familiarDisponible.append(self)
            barreraListos.acquire()## Barrera  para verificar que todos estén listos para iniciar
            if cuentaListos == cantidad_personas:
                barreraListos.release() #Liberamos la barrera
           
        else:
            mutexFamiliar.acquire()
            if random.random() < 0.1: # Si llega un 
                print_fail("Ups!, a "+self.parentesco+str(self.numero)+" le dio coronavirus 😷")
                print("   ------------------    ")
                print("     !!! ALERTA !!!     ")
                print("   ------------------    ")
                coronaviroso.acquire()
                time.sleep(0.5)# Si hay alguien con coronavirus paramos todo
                coronaviroso.release()
                print_warn("Yeih!, "+self.parentesco+str(self.numero)+" se ha recuperado! 😀")
                familiarDisponible.append(self)
                mutexFamiliar.release()
            else:
                familiarDisponible.append(self)
                mutexFamiliar.release()

    def Trabajar(self,nombreTarea):
        global mutexTarea, familiarDisponible 
        self.descanso.release()## Lo sacamos del descanso
        print_info(self.parentesco+str(self.numero)+" está trabajando en "+nombreTarea)
        time.sleep(random.random()) ## Tiempo en que tarda hacer una tarea una persona
        print(self.parentesco,self.numero,'dejó de trabajar en',nombreTarea)
        self.entrarDisponible(nombreTarea)



class Casa:
    def __init__(self, cantidad_personas, tareasdelDia):
        global listaDeTareas, familiarDisponible 
        for x in range(cantidad_personas):
            ## Lanzamos todos los hilos de personas para que se enlisten a personas listas, con random hacemos que sean aleatorios sus parentescos
            threading.Thread(target = Persona, args=[x,parentescos[random.randrange(10)]]).start()
        
        for y in range(tareasdelDia):
            requeridosParalaTarea = random.randrange(1,4)
            posibilidad = DiccionarioTareas[requeridosParalaTarea]
            ## Damos tareas aleatorias del diccionario por lo que pueden repetirse, al igual que algunas ocupan 1,2 o 3 personas para realizarse
            nombreTarea = random.choice(posibilidad)
            mutexTarea.acquire()          
            listaDeTareas.append(threading.Thread(target = Tarea, args= [y, requeridosParalaTarea,nombreTarea]).start())
            mutexTarea.release()
            mutexTarea.acquire()
            mutexTarea.release()


##Funciones para imprimir con diferente formarto: Rojo fail, Verde pass, Info azul, amarillo warn y para hacer un banner sencillo

def banner(texto, ch='=', length=78):
    textoEspaciado = ' %s ' % texto
    banner = textoEspaciado.center(length, ch)
    return banner


def print_fail(message, end = '\n'):
    sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)


def print_pass(message, end = '\n'):
    sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)


def print_warn(message, end = '\n'):
    sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)


def print_info(message, end = '\n'):
    sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)


if __name__ == '__main__':
    print("\n")
    print("\t"+banner("Bienvenido seas a")+"\n")
    print("                 ☆ ∩∩ （ • •）☆")
    print("     ┏━∪∪━━━━━━━━━━━━━━━━━━━━━┓")
    print("         ☆🧹 CUARENTENA 🐶 ☆")
    print("     ┗━━━━━━━━━━━━━━━━━━━━━━━━┛﻿")
    print("\n")
    cantidad_personas = int(input("Por favor ingrese la cantidad de personas que hay en este hogar: "))
    tareasdelDia = int(input("Ingrese la cantidad de tareas que habrá en el hogar: "))
    cuarentena = Casa(cantidad_personas,tareasdelDia)


