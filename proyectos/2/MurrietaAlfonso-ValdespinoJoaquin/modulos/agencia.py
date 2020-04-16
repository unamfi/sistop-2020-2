from threading import RLock, Thread
from time import sleep
import sys

from modulos.compania import compania


class agencia(object):

    def __init__(self, companias: [compania], varN:str,numClientes ):
        #mutex para las acciones de la agencia
        global agLock
        agLock = RLock()
        agLock.acquire()
        self.nombre = varN
        self.companiaList = companias
        self.disponibles = []
        self.iniDatos()
        self.numC = numClientes
        agLock.release()

    def actualizar(self):
        try:
            global agLock
            agLock.acquire()
          
            self.disponibles.clear()
            for comp in self.companiaList:
                asientosCompania = comp.getAsientosDisponibles()
                for asiento in asientosCompania:
                    self.disponibles.append((comp , asiento.num , comp.getPrecioActual()))
            #print('-Actualizacion'+'\a') 
            sleep(1)
            agLock.release()
            return True
        except:
            print('# Excepcion al realizar la actualización :(' + self.nombre)
            agLock.release()

    def autoActualizar(self):
        count=0
        while(True):
            sleep(4)
            #print("autoactualiza"+self.nombre)
            count+=1
            if (count>self.numC+1):
                print(self.nombre+ " ha dejado de operar.")
                sys.exit()
            if not (self.actualizar()):
                sleep(0.5)
                self.actualizar()
                

    def iniDatos(self):
        self.disponibles.clear()
        for comp in self.companiaList:
            for asiento in comp.asientos:
                self.disponibles.append((comp, asiento.num, comp.getPrecioActual()))

    def getList(self):
        global agLock
        agLock.acquire()
        asientoList = self.disponibles
        agLock.release()
        return asientoList

    def run(self):
        print('Iniciando ' + self.nombre)
        Thread(target= self.autoActualizar).start()
        return True
    

    def vender_Cliente(self, comp: compania, asiento: int):
        
        global agLock
        agLock.acquire()
        #print('\Vendiendo')

        for companiaDeseada , asientoDeseado, v  in self.disponibles:
            if companiaDeseada == comp and asientoDeseado == asiento:
                break
        try:
            if(companiaDeseada.venderAsiento(asientoDeseado)):
                print("\n####################################################")
                print('#Agencia: ', self.nombre, ' | Compania: ' ,  companiaDeseada, ' | Asiento: ', asientoDeseado, ' | Precio: ', companiaDeseada.precioActual,"\a")
                #print('\n#Agencia: ', self.nombre, ' | Compania: ' ,  companiaDeseada, ' | Asiento: ', comp.asiento.index , ' | Precio: ', companiaDeseada.precioActual)
                print("####################################################\n")
                agLock.release()
                sleep(0.1)
                self.actualizar()
                return True

            else:
                print('   ', self.nombre,' no pudo vender a:',  companiaDeseada,' el asiento ', asientoDeseado)
                print('     [Asiento no disponible - Vendido actualmente]')
                agLock.release()
                sleep(0.1)
                return False

        except:
            print('# Excepcion originada de venta cliente ' + self.nombre)
            #agLock.release()
            return False
        