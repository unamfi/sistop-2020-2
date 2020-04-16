# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 02:52:43 2020

@name: El plato de comida para perros
@author: Fernando Arturo Medina Molina
@contact: fernando170@comunidad.unam.mx
@version: 1.0
@description:
    A través de éste código se pretende dar solución al problema de 
    sincronización de hilos planteado en el archivo README.md dentro de este 
    repositorio, las variables se explicaran en el apartado @variables, para
    resolver la problemática planteada he decidido utilizar el más común de las
    implementaciónes que es la de hacer un mutex con la finalidad de que el 
    alimento pueda restarsele la cantidad de alimento que el perro desee en 
    cada ocasión.
    
@variables:
    cantidadDeCroquetas: Será la cantidad en gramos de comida que se le da a 
                         los perros. :int:
    perroG: Será la representación del perro más grande como un hilo y podrá 
            comer hasta 300 gramos por ocasión.
    perroM: Será la representación del perro mediano de igual manera con un 
            hilo, este podrá consumir hasta 100 gramos.
    perroC: Será la representación del perro pequeño igualmente con un hilo, el
            cual puede consumir hasta 50 gramos de alimento por ocasión.
    plato: Será el recurso que se compartirá por los perros, en el está 
           contenido la cantidad de alimento servida en esa ocasión.
    tDeCons: Tiempo que tardará el perro en consumir su alimento. :int:
        
"""

import threading
import time

cantidadDeCroquetas=450

def consumo(cantidad,tDeCons,perro):
    """
    Una vez que el perro se acerque al plato y lo posea, éste podrá consumir la
    cantidad adecuada establecida por su tamaño.
    :param cantidad: Será la cantidad de alimento que consume el perro en esa 
    ocasión:int
    """
    global cantidadDeCroquetas
    print('El perro '+perro+' está comiendo')
    time.sleep(tDeCons)
    cantidadDeCroquetas=cantidadDeCroquetas - cantidad
    print('Cantidad de croquedas actual: '+str(cantidadDeCroquetas)+' gramos\n\n\n')
    if cantidadDeCroquetas==0:
        print('Ya no quedan croquetas!!! a ladrar para que nos hagan caso.')

def comer(plato,cantidad,tDeCons,perro):
    '''
    El perro en acercarse primero, será el que tenga la oportunidad de 
    alimentarse en ese momento ya que poseerá el plato.
    :param plato: Simulará la función del plato, ya que solo existe uno y es al
    que se le quitará la comida que les fue suministrada.:recurso protegido
    :param cantidad: será la cantidad de comida consumida en esta ocasión por 
    el perro, variará según su tamaño:int 
    '''
    plato.acquire()#Adquisición del plato
    consumo(cantidad,tDeCons,perro)#Llamada a la función consumo
    plato.release()#El perro ahora está satisfecho, puede ir a descansar
    
print('Plato servido!!! A comer!')
print('Cantidad de croquetas actual: '+str(cantidadDeCroquetas)+' gramos\n\n\n')
plato=threading.Lock()#El plato será el recurso protegido
perroG=threading.Thread(target=comer,args=(plato,300,5,'grande'))
perroM=threading.Thread(target=comer,args=(plato,100,3,'mediano'))
perroC=threading.Thread(target=comer,args=(plato,50,2,'chico'))

perroG.start()
perroM.start()
perroC.start()

perroG.join()
perroM.join()
perroC.join()