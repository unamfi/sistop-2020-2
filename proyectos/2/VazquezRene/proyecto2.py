#!/usr/bin/python
# -*- coding: utf-8 -*-
# Sistemas Operativos 
# Rene Vazquez Peñaloza 


import random
import threading
import time

#En esta variable se define en numero de clientes que puede haber conectados al servidor
UsuariosConectados=2
#Se definen los multiplex que nos permiten controlar el flujo en cada direccion
multiplexConsulta = threading.Semaphore(UsuariosConectados)
multiplexGuardar = threading.Semaphore(UsuariosConectados)

def esSeguroConsultar():
    if (numUsuariosGuardando - (numUsuariosConsultando + 1)) == 0:
        return False
    return True

def esSeguroGuardar():
    if (numUsuariosConsultando - (numUsuariosGuardando + 1)) == 0:
        return False
    return True

#Estas variables nos permiten decidir si es seguro consultar o guardar. 
numUsuariosConsultando = 0
numUsuariosGuardando = 0
mutexAGuardar = threading.Semaphore(0)
mutexAConsulta = threading.Semaphore(0)
sepuedeConsultar = esSeguroConsultar()
sepuedeGuardar = esSeguroGuardar()

#Con 1 Consulta con 0 Guarda 
def elegirAccion():
        if random.random() < 0.5:
            return 1
        else:
            return 0

AConsulta=set()
AGuardar = set()
Lectura = set()
class Usuario():
    
    def __init__(self, nombre):
        global numUsuariosGuardando
        global numUsuariosConsultando
        

        self.nombre = nombre
        self.accionActual = -1
        #print(self.nombre + " está en espera")
        self.isWaiting = True
        Lectura.add(self)

    def __str__(self):
        accion =  "de consulta" if self.accionActual == 1 else "de guardar"
        return self.nombre + " está realizando " + accion
    

    def eventos(self):
        global numUsuariosGuardando
        global numUsuariosConsultando
        global sepuedeGuardar
        global sepuedeConsultar
        """mutexAGuardar.acquire()
        sepuedeConsultar = esSeguroConsultar()
        mutexAGuardar.release()
        mutexAGuardar.acquire()
        sepuedeGuardar = esSeguroGuardar()
        mutexAGuardar.release()"""

        itera = 1
        while(True):
            nuevaAccion = elegirAccion()
            if nuevaAccion == self.accionActual:
                tmp =  "de sentido del reloj" if self.accionActual == 1 else "contra reloj"
                
                continue
            if self.isWaiting:
                Lectura.remove(self)
                if nuevaAccion == 1 and itera == 1 and sepuedeConsultar:
                     #Quiere decir que la accion que realizaba era consulta
                    multiplexConsulta.acquire()
                    AConsulta.add(self)
                    self.accionActual = 1
                    self.isWaiting = False
                    numUsuariosConsultando+=1
                    #print(self)
                    continue   
                elif nuevaAccion  == 0 and itera == 1 and sepuedeGuardar:
                    multiplexGuardar.acquire()
                    AGuardar.add(self)
                    self.accionActual = 0
                    self.isWaiting = False
                    numUsuariosGuardando+=1
                    #print(self)
                    continue

                if nuevaAccion == 1:
                    
                    multiplexGuardar.release()
                    AGuardar.remove(self)

                elif nuevaAccion  == 0:
                    multiplexConsulta.release()
                    AConsulta.remove(self)  


                if nuevaAccion == 1 and sepuedeConsultar:
                     
                    multiplexConsulta.acquire()
                    AConsulta.add(self)
                    self.accionActual = 1
                    self.isWaiting = False
                    numUsuariosConsultando+=1
                    numUsuariosGuardando -= 1
                    #print(self)

                elif nuevaAccion  == 0 and  sepuedeConsultar:
                    multiplexGuardar.acquire()
                    AGuardar.add(self)
                    self.accionActual = 0
                    self.isWaiting = False
                    numUsuariosGuardando+=1
                    numUsuariosConsultando -= 1
                    #print(self)
                else:
                    Lectura.add(self)
                    self.isWaiting = True
                    
    
            elif not self.isWaiting:
                Lectura.add(self)
                self.isWaiting  = True
                            
            itera += 1
            time.sleep(5)
            
                
def getStatus():
    while(True):
        string="************************************\n"
        string += "Usuarios consultando[ " + "*"*len(AConsulta)+" ]\n"
        for Usuario in AConsulta:
            string += " ** "+Usuario.nombre+"\n"
        string += "Usuarios guardando[ " + "*"*len(AGuardar)+" ]\n\n"
        for Usuario in AGuardar:
            string += " ** "+Usuario.nombre+"\n"
        time.sleep(5)
        print(string)

def main():
    rene = Usuario("Rene")
    bruno = Usuario("Bruno")
    daniel = Usuario("Daniel")
    diego = Usuario("Diego")
    rafael = Usuario("Rafael")
    edith = Usuario("Edith")
    cliente=[rene, bruno, daniel, diego, rafael, edith]
    print("*"*30)
    hilos = []
    hilos.append(threading.Thread(target=getStatus))

    for usuario in cliente:
        hilo = threading.Thread(target=usuario.eventos)
        hilos.append(hilo)

    for hilo in hilos:
        hilo.start()

if __name__ =="__main__":
   main()