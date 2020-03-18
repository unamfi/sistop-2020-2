#SISTEMAS OPERATIVOS
#EJERCICIOS DE SINCRONIZACION - GATOS Y RATONES
#Murrieta Villegas Alfonso y Valdespino Mendieta Joaquín

import threading

###########Declaración de variables#############################

#MUTEX para proteger a los gatos y ratones
mutexM = threading.Semaphore(1)
mutexC = threading.Semaphore(1)

#Mediante un APAGADOR cumpliremos la condición más relevante que es "Ningún gato puede acercarse si un ratón está comiendo"
#DUDA: ¿ Estos gatos y ratones viven en una utopía democrática ?
canEat = threading.Semaphore(1) 

#NOTA 1 -> Modificar la variable numPlat dependiendo de la cantidad de platos que se requiera probar 
#NOTA 2 -> Se usará un MULTIPLEX debido a que solamente un gato o ratón puede comer en un plato
numDish = threading.Semaphore(10) 

#Inicialización de la cantidad de ratones y gatos
mice= 0
cats = 0


#NOTA 3: Se crearán 2 clases debido a que se utilizará el paradigma orientado a objetos para facilitar la descripicón de cada animal
########### Clases de gato y ratón #############################


class mouse:

    def __init__(self, numMice):
        self.numMice = numMice

        #Variable para saber si está vivo o muerto <- Posteriormente la usaremos para ver si los gatos se come al ratón o no 
        self.alive = True

        print("RATON: %d-- EDO: Iré a comer" % (numMice))
        self.eat()

    def eat(self):
        global mice, cats

        numDish.acquire()
        mutexM.acquire()
        mice += 1

        #Utilizamos el APAGADOR para indicar que están comiendo los ratones <- Paso portal en el código
        if mice == 1:
            canEat.acquire()
        mutexM.release()
        print("RATON: %d-- EDO: Estoy comiendo" % (self.numMice))


        #Verificamos el estado en el que se encuentra nuestro ratón ()      
        mutexC.acquire()
        if(cats > 0):
            self.alive = False
        mutexC.release()

        if(self.alive == True):
            print("RATON: %d-- EDO: Ya comí :D y sigo vivo! " % (self.numMice))                
        else:
            print("RATON: %d-- EDO: MUERTO " % (self.numMice))      


        mutexM.acquire()
        mice-=1

        #Utilizamos nuevamente el APAGADOR <- Terminamos el paso mortal previamente mencionado
        #Lo que hacemos aquí es liberar el apagador 
        if mice == 0:
            canEat.release()
        mutexM.release()
        numDish.release()



class cat():

    def __init__(self, numCats):
        self.numCats = numCats
        print("GATO: %d -- EDO: Iré a comer" % (self.numCats))
        self.eat()

    def eat(self):
        global cats

        #Primero válidamos si podemos comer, permitimos que coman los ratones y por último escoge en que plato comerá
        canEat.acquire()
        canEat.release()
        numDish.acquire()

        #El gato va a comer
        print("GATO: %d -- EDO: Estoy comiendo" % (self.numCats))        
        mutexC.acquire()
        cats = cats +1
        mutexC.release()
        
        #El gato ya ha terminado de comer
        print("GATO: %d -- EDO: He terminado de comer" % (self.numCats))
        mutexC.acquire()
        cats = cats -1
        mutexC.release()
        numDish.release()





########### Instancia de hilos y solicitud de cantidad de gatos y ratones #############################
num_gatos = int(input("Ingrese el número de gatos: "))
num_ratones = int(input("Ingrese el número de ratones: "))

for i in range(num_gatos):
    threading.Thread(target=cat, args=[i]).start()

for i in range(num_ratones):
    threading.Thread(target=mouse, args=[i]).start()


















