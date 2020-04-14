from threading import RLock, Thread
from time import sleep

from modulos.compania import compania


class agencia(object):
    def __init__(self, companias: [compania], varN:str ):
        #mutex para las acciones de la agencia
        global agLock
        agLock = RLock()
        agLock.acquire()
        self.nombre = varN
        self.companiaList = companias
        self.disponibles = []
        self.iniDatos()
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
            #print('-Update'+'\a') # Sound ALert
            sleep(1)
            agLock.release()
        except:
            print('excepcion al realizar la actualización ' + self.nombre)
            agLock.release()

    def autoActualizar(self):
        while(True):
            sleep(5)
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
        print('Starting run ' + self.nombre)
        Thread(target= self.autoActualizar).start()

        return True

    def vender_Cliente(self, comp: compania, asiento: int):
        #print('\nTrying to sell')
        global agLock
        agLock.acquire()
        #print('\nSelling')
        for companiaDeseada , asientoDeseado, v  in self.disponibles:
            if companiaDeseada == comp and asientoDeseado == asiento:
                break
        try:
            if(companiaDeseada.venderAsiento(asientoDeseado)):
                print("\n####################################################")
                print('\n', self.nombre, ' vendido:' ,  companiaDeseada, 'el asiento', asientoDeseado, 'a', companiaDeseada.precioActual )
                print("####################################################\n")
                agLock.release()
                sleep(0.1)
                self.actualizar()
                return True
            else:
                print('\n', self.nombre,' fallo al vender:',  companiaDeseada,'el asiento ', asientoDeseado, ' (Vendido actualmente)')
                agLock.release()
                sleep(0.1)
                return False
        except:
            print('excepcion originada de venta cliente ' + self.nombre)
        #    agLock.release()
            return False