from random import randrange
from threading import RLock
from time import sleep

class Asiento(object):
    def __init__(self, index:int):
        self.num = index
        self.disponible = True

    def __int__(self):
        return self.num

    def __str__(self):
        return str(self.num)

class compania(object):
    def __init__(self, varN: str):
        global cpLock
        cpLock = RLock()
        cpLock.acquire()
        self.nombre = varN
        self.cantidadAsientos = 5
        self.Asientosdisponibles = 0
        self.asientos = []

        for i in range(self.cantidadAsientos):
            self.asientos.append(Asiento(i))
            self.Asientosdisponibles+=1
        self.precioBase = 250.00
        self.precioActual = self.precioBase + randrange(0,50,2)
        cpLock.release()

    def __str__(self):
        return self.nombre

    def getPrecioActual(self):
        global cpLock
        cpLock.acquire()
        precio = self.precioActual
        cpLock.release()
        return precio

    def getAsientosDisponibles(self):
        global cpLock
        cpLock.acquire()
        list = []
        if self.Asientosdisponibles > 0:
            for asiento in self.asientos:
                if asiento.disponible:
                    #print(asiento)
                    list.append(asiento)
            cpLock.release()
            return list
        else:
            cpLock.release()
            return list

    def venderAsiento(self, asientoNum):
        global cpLock
        cpLock.acquire()
        if self.asientos[asientoNum].disponible :
            self.asientos[asientoNum].disponible = False
            self.Asientosdisponibles -=  1
            self.aumentarPrecio()
            cpLock.release()
            return True

        else: #segundo intento
            sleep(1)
            if self.asientos[asientoNum].disponible :
                self.asientos[asientoNum].disponible = False
                self.Asientosdisponibles -= 1
                self.aumentarPrecio()
                cpLock.release()
                return True
            else:
                cpLock.release()
                self.manager()
                return False

    def aumentarPrecio(self):
        self.precioActual += self.precioActual * 0.1

    #Parte encargada de mostrar concurrencias -> Es la solución del generente al tener fallo en la venta del boleto
    #El problema de concurrencia se puede ver en la clase agencia, método vender_Cliente
    def manager(self): 
        global cpLock
        cpLock.acquire()
        if  not self.Asientosdisponibles  == self.cantidadAsientos:
            print("\n-> El manager loco ha subido los precios de ",self.nombre ," | Asientos disponibles: ",self.Asientosdisponibles,"\n")
            
            for i in range(self.Asientosdisponibles):#Consideraremos la cantidad de asientos para el incremento en el precio
                self.aumentarPrecio() 
        cpLock.release()