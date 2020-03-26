from random import randint
from time import sleep
import copy
import sys

class Process:

    def __init__(self, id, time, t_llegada):
        self.id = id 
        self.time = time # Duración del Proceso
        self.t_restante = self.time # Tiempo que le resta a un proceso de ejecucion
        self.t_inicio = 0 # Tiempo en que el proceso comenzo su ejecucion
        self.t_fin = 0  # Timpo en que el proceso termina su ejecucion
        self.E = 0 # Tiempo en Espera
        self.T = 0 # Tiempo en Respuesta
        self.P = 0 # Proporcion de Penalización 
        self.t_llegada = t_llegada # Momento en que un proceso llega para ser procesado

    def setT(self): 
        self.T = self.t_fin - self.t_llegada
        return self.T

    def setE(self):
        self.E = self.T - self.time
        return self.E
        
    def setP(self):
        self.P = self.T / self.time
        return self.P

class PLANIFICADORES:

    numProcess = 0
    buffer = ""
    procesos_ejecutados = []
    time = 0

    def __init__(self, queue, nq, p):
        self.queue = queue
        self.numProcess = len(self.queue)
        self.FIFO(copy.deepcopy(self.queue))
        self.RR(nq, copy.deepcopy(self.queue))
        self.SRR(copy.deepcopy(self.queue))
        self.SPN(copy.deepcopy(self.queue))
        self.FB(copy.deepcopy(self.queue),p)
    
    def PrintTable(self, listaProcess):
        print("+-------------------------------------------------------------+")
        print('{8} {0:10s} {8} {1:9s} {8} {2:2s} {8} {3:5s} {8} {4:3s} {8} {5:2s} {8} {6:2s} {8} {7:4s} {8}'.format("Proceso", "Llegada", "t", "Inicio", "Fin", "T", "E", "P", u'\u00A6'))
        print("+-------------------------------------------------------------+")
        for i in listaProcess:
            print('{8} {0:10s} {8} {1:9d} {8} {2:2d} {8} {3:6d} {8} {4:3d} {8} {5:2d} {8} {6:2d} {8} {7:4.2f} {8}'.format(i.id, i.t_llegada, i.time, i.t_inicio, i.t_fin, i.T, i.E, i.P, u'\u00A6'))
        print("+-------------------------------------------------------------+")


    def getProcess(self, listaProcess, t):
        # Regresa al proceso que llego en el tiempo t
        if(listaProcess and listaProcess[0].t_llegada == t):
            return listaProcess.pop(0) 
    
    def reset(self):
        # Reiniciamos las estructuras
        self.buffer = ""
        self.procesos_ejecutados = []
        self.time = 0
    
    def Estadisticas(self, Algoritmo):
        meanT = 0
        meanE = 0
        meanP = 0
        for process in self.procesos_ejecutados:
            #Para cada proceso ejecutado se obtiene su T, E y P
            meanT += process.setT()
            meanE += process.setE()
            meanP += process.setP()
        #Se obtienen los promedios por planificador de procesos
        meanT /= self.numProcess
        meanE /= self.numProcess
        meanP /= self.numProcess
        print("%s: T = %.1f, E = %.1f, P = %.1f" %(Algoritmo, meanT, meanE, meanP))
        print(self.buffer)
        #self.PrintTable(self.procesos_ejecutados)
        self.reset()


    def FIFO(self, listaProcess):
        queue = [] # Cola de procesos en espera
        queue.append(listaProcess.pop(0))
        while queue: 
            #Mientras haya procesos en la cola
            process = queue.pop(0)
            process.t_inicio = self.time # Establecemos el tiempo de inicio del proceso
            while process.t_restante:
                # Mientras el proceso no termine su ejecucion
                self.time += 1
                process.t_restante -= 1
                self.buffer += process.id
                # Identificamos si en ese instante de tiempo ha llegado un proceso nuevo:
                processNuevo = self.getProcess(listaProcess, self.time)
                if(processNuevo):
                    # De ser así entra en la cola
                    queue.append(processNuevo)
            # Termiando el proceso establecemos en que momento termino
            process.t_fin = self.time
            # Añadimos el proceso a la lista procesos_ejecutados para generar las estadisticas
            self.procesos_ejecutados.append(process) 
        self.Estadisticas("FIFO") # Mostramos las estadisticas de FIFO
        

    
    
    def RR(self, qn, listaProcess): # nq quantums de ejecución
        queue = [] # Cola de procesos
        queue.append(listaProcess.pop(0))
        while queue:
            # Mientras la cola tenga procesos en espera
            process = queue.pop(0)
            if(process.t_restante == process.time):
                # Si es la primera vez que el proceso es ejecutado, se asigna su tiempo de inicio
                process.t_inicio = self.time
            i = 0 # numero de quantum completados 
            while (i < nq and process.t_restante):
                # Mientras no se complete el proceso o su numero de quantums 
                i += 1
                self.time += 1
                process.t_restante -= 1 # Actualizamos el tiempo restante
                self.buffer += process.id
                # Identificamos si en ese instante de tiempo ha llegado un proceso nuevo:
                processNuevo = self.getProcess(listaProcess, self.time)
                if(processNuevo):
                    # De ser así los proceses entran a la cola
                    queue.append(processNuevo)
            if process.t_restante:
                # Si el proceso no ha terminado su ejecucion se encola nuevamente
                queue.append(process)
            else:
                # Si el proceso ya termino su ejecucion se registra el tiempo y se guarda el proceso para su analisi estadistico
                process.t_fin = self.time
                self.procesos_ejecutados.append(process)
        self.Estadisticas("RR" + str(nq))


    def SRR(self, listaProcess, a = 1, b = 2): 
        # a -> ritmo de crecimiento de la cola de de procesos nuevos
        # b -> ritmo de incremento de prioridad en la cola de procesos aceptados
        queueAceptados = []
        prioridadAceptados = 0 # Prioridad de los procesos aceptados
        queueNuevos = []    
        queueAceptados.append(listaProcess.pop(0))
        while queueAceptados:
            # Mientras haya procesos aceptados
            process = queueAceptados.pop(0)
            if process.t_restante == process.time:
                # Si es la primera vez que el proceso es ejecutado, se registra su tiempo de inicio
                process.t_inicio = self.time
            self.time += 1
            self.buffer += process.id
            process.t_restante -= 1 # Actualizamos el tiempo restante
            prioridadAceptados += a # Incrementamos en 'a' la prioridad de los procesos
            # Identificamos si en ese instante de tiempo ha llegado un proceso nuevo:
            processNuevo = self.getProcess(listaProcess, self.time)
            if(processNuevo):
                # Agregamos a la cola de proceso nuevos el proceso
                queueNuevos.append(processNuevo)
            if (queueNuevos and (self.time - queueNuevos[0].t_llegada) * b == prioridadAceptados):
                # Si el proceso al inicio de la cola tiene la prioridad de un proceso acetado, lo encolamos en queueAceptados
                queueAceptados.append(queueNuevos.pop(0))
            if process.t_restante:
                # Si el proceso aún no termina su ejecucion, se vuelve a encolar
                queueAceptados.append(process)
            else:
                # Si el proceso ya termino su ejecucion se registra el tiempo y se guarda el proceso para su analisi estadistico
                process.t_fin = self.time
                self.procesos_ejecutados.append(process)
            if not queueAceptados and queueNuevos:
                # En caso de que la cola no tenga procesos aceptados y existan procesos en espera
                queueAceptados.append(queueNuevos.pop(0))
        self.Estadisticas("SRR") 
                

    
    def SPN(self, listaProcess):
        queue = [] # Cola de procesos
        self.EnqueueSPN(queue, listaProcess.pop(0))
        while queue:
            # Mientras haya procesos en espera
            process = queue.pop(0)
            process.t_inicio = self.time # Registramos el tiempo de inicio del proceso
            while process.t_restante:
                # Mientras el proceso no termine su ejecución
                self.time += 1
                process.t_restante -= 1 
                self.buffer += process.id
                # Identificamos si en ese instante de tiempo ha llegado un proceso nuevo:
                processNuevo = self.getProcess(listaProcess, self.time)
                if(processNuevo):
                    # Encolamos el proceso de acuerdo a su tiempo de ejecucion, funcion EnqueueSPN
                    self.EnqueueSPN(queue, processNuevo)
            process.t_fin = self.time # Rregistramos el tiempo de finalizacion del proceso
            self.procesos_ejecutados.append(process) # Agregamos el proceso a la lista para su analisis estadistico
        self.Estadisticas("SPN")
    
    def EnqueueSPN(self, queue, process):
        # Permite generar una politica de insercion de cola de prioridad
        if not queue:
            # Si la cola esta vacía, se encola por defecto el proceso
            queue.append(process)
        else:
            for j in range (0, len(queue)):
                # Recorremos cada elemento de la cola
                if process.time < queue[j].time:
                    # Si el tiempo del proceso a encolar es menor que la del elemento j, se encola el proceso en esa posición
                    queue.insert(j,process)
                    break
                if(j + 1 == len(queue)):
                    # Si llegamos al ultimo elemento en la cola, el proceso tiene el mayor tiempo
                    queue.append(process)
                    break

    def FB(self, listaProcess, numQueue = 5):
        # numQueue número de colas de prioridad
        queue = [[] for i in range(0, numQueue)] # Inicializamos las 'n' colas dentro de queue
        queue[0].append(listaProcess.pop(0)) # El primer proceso entra a la cola de mayor prioridad
        repetir = True
        while repetir:
            # Mientras de cumpla la bandera
            repetir = False
            for i in range(0, len(queue)):
                # Para cada cola de prioridad contenida en queue
                q = pow(2, i) # Número de quantum de acuerdo a la prioridad de la cola: 1, 2, 4, 8, ...
                while queue[i]:
                    # Para cada proceso en la cola de prioridad 'i'
                    process = queue[i].pop(0)
                    if(process.t_restante == process.time):
                        # Si el la primera vez que se ejecuta el proceso se registra su tiempo de inicio
                        process.t_inicio = self.time
                    j = 0 # numero de quantums de ejecucion que lleva cada proceso
                    while( j < q and process.t_restante):
                        #print(process.id, q)
                        self.time += 1
                        j += 1
                        self.buffer += process.id
                        process.t_restante -= 1 
                        # Identificamos si en ese instante de tiempo ha llegado un proceso nuevo:
                        processNuevo = self.getProcess(listaProcess, self.time)
                        if(processNuevo):
                            # En caso de haberlo se encola en la cola de maxima prioridad
                            queue[0].append(processNuevo)
                            repetir = True # Se activa la bandera para repetir el algortimo
                    if(process.t_restante):
                        # Si el proceso no ha terminado su ejecución, este se degrada a la siguiente cola
                        if(i == numQueue - 1):
                            queue[i].append(process)
                        else:
                            queue[i + 1].append(process)
                    else:
                        # Si el proceso a finalizado su ejecución, se registra su tiempo de fin
                        process.t_fin = self.time
                        self.procesos_ejecutados.append(process)
                    if(repetir):
                        # Sí de ha llego un proceso de prioridad 0, se tiene que atender antes de continuar
                        break
                if(repetir):
                    # Sí de ha llego un proceso de prioridad 0, se tiene que atender antes de continuar a la siguiente cola
                    break
        self.Estadisticas("FB")  

    
if __name__ == '__main__':
    lista =[] # Lista de procesos
    t_i = 0 # Tiempo de llegada del primer proceso
    time = 0 
    arg = sys.argv
    np = int(arg[1]) if len(arg) == 2 else 5 # Número de procesos
    nq = int(arg[2]) if len(arg) == 3 else 2 # Número de quantums (RR)
    p = int(arg[3]) if len(arg) == 4 else 5  # Número de Colas de (FB)
    for i in range(0,np):
        time = randint(1, 10) # tiempo aleatorio de cada proceso
        lista.append(Process(chr(i + 65), time, t_i))
        t_i += randint(1 , time) # tiempo de llegada determinado aleatoriamente, dos procesos no pueden llegar al mismo tiempo
    PLANIFICADORES(lista, nq, p) # LLamada a los planificadores