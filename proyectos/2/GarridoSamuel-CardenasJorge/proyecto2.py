import threading 
import sys
import random
import time

parentescos = ['👨 Papá','👩‍🦱 Mamá','👶 Bebe','👦 Niño','👧 Niña','👱‍♀️ Adolescente','🧑 Joven','👴 Abuelo','👵 Abuela','🐕 Perro','🐈 Gato']
DiccionarioTareas = {1:['Ordenar la cama 🛌','Acomodar la mesa 🍴','Lavar el baño 🚽','Barrer 🧹','Trapear 🧹','Sacudir 💨','Planchar 👕'],2:['Lavar la ropa 🧼','Cocinar 🥘','Ordenar el librero 📚','Lavar los trastes 🍽'],3:['Ordenar la bodega 🗄','Podar el jardín 🌳']}
mutexTarea = threading.Semaphore(1)
mutexFamiliarT = threading.Semaphore(0)
mutexFamiliar = threading.Semaphore(1)
familiarDisponible =[]
listaDeTareas =[]
cantidad_personas = 5
tareasdelDia = 5
tareas = threading.Semaphore(tareasdelDia)
personas = threading.Semaphore(cantidad_personas)
cuentaListos = 0
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
        ##
        listaDeTareas.pop(0)
        self.realizarse(self.numero,self.nombreTarea,self.requeridosParaUnaTarea)
        ##
        mutexTarea.release()

    def realizarse(self,numero,nombreTarea,requeridosParalaTarea):
        global personas, familiarDisponible, cantidad_personas
        requeridos = []
        for i in range(requeridosParalaTarea):
            personas.acquire()
            mutexFamiliar.acquire()
            requeridos.append(familiarDisponible.pop(random.randrange(len(familiarDisponible))))
            mutexFamiliar.release()
            mutexFamiliar.acquire()
            mutexFamiliar.release()
        for i in requeridos:
            i.Trabajar(nombreTarea)
        while True:
            if all(elem in familiarDisponible for elem in requeridos):
                print('\n\t',requeridosParalaTarea,'ha(n) terminado la tarea:',nombreTarea,'\n')
                self.barrera.release()
                self.barrera.acquire()
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
        global cuentaListos,barreraListos,mutexListos
        if nombreTarea == 'vacio':
            mutexFamiliar.acquire()

            cuentaListos = cuentaListos + 1
            print_pass(str(self.parentesco)+str(self.numero)+' está listo para el trabajo')
            mutexFamiliar.release()
            mutexFamiliar.acquire()
            mutexFamiliar.release()
            familiarDisponible.append(self)
            barreraListos.acquire()
            if cuentaListos == cantidad_personas:
                barreraListos.release()
            
        else:
            mutexFamiliar.acquire()
            if random.random() < 0.1:
                print_fail("Ups!, a "+self.parentesco+str(self.numero)+" le dio coronavirus 😷")
                print("   ------------------    ")
                print("     !!! ALERTA !!!     ")
                print("   ------------------    ")
                coronaviroso.acquire()
                time.sleep(0.5)
                coronaviroso.release()
                print_warn("Yeih!, "+self.parentesco+str(self.numero)+" se ha recuperado! 😀")
                familiarDisponible.append(self)
                mutexFamiliar.release()
            else:
                familiarDisponible.append(self)
                mutexFamiliar.release()

    def Trabajar(self,nombreTarea):
        global mutexTarea, familiarDisponible
        self.descanso.release()
        print_info(self.parentesco+str(self.numero)+" está trabajando en "+nombreTarea)
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
            mutexTarea.acquire()
            mutexTarea.release()




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

def print_bold(message, end = '\n'):
    sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)


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


