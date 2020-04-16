"""
    Proyecto 2: Una situación cotidiana paralelizable
    Alumnos:
        Barcenas Avelas Jorge Octavio
        Reza Chavarria Sergio Gabriel
    Profesor:
        Gunnar Eyal Wolf Iszaevich
"""
import threading
import random
from tkinter import *
raiz=Tk()

#####################Variables globales########################

#meseros, chefs, mesas, clientes
meserosSTR=StringVar()
mesasSTR=StringVar()
chefsSTR=StringVar()
clientesSTR=StringVar()
num_meseros=0
num_mesas=0
num_chefs=0
num_clientes=0



#####################Clases######################################
###########listas
meserosDisponibles = []
clientesEnEspera = [] 
chefsDisponibles = []

## Mutex para los chefs y meseros disponibles y fila de clientes en espera
mutex_fila_espera = threading.Semaphore(1)
mutex_meseros_disp = threading.Semaphore(1)
mutex_chefs_disp = threading.Semaphore(1)

## Multiplex para chefs, mesa, meseros disponibles
chefs = threading.Semaphore(num_chefs)
meseros = threading.Semaphore(num_meseros)
mesas = threading.Semaphore(num_mesas)



#############################################################
#Codigo de la interfaz
#############################################################



"""Parametros iniciales para la ventana"""
raiz.title("Le Restaurante")
raiz.resizable(False, False)
raiz.geometry("850x650")
raiz.config(bg="beige")

Label(raiz,text="Bienvenido al \"Le Restaurant\"",bg="White",font=("Imprint MT Shadow",20)).place(x=300,y=30)

#Creación de frame para la ventana, este frame será utilizado para resguardar los texto, cuadros de texto y boton para el ingreso de cantidades.
Frame1=Frame()
#Configuración del frame 1
Frame1.config(bg="Red")
Frame1.config(bd=10)
Frame1.config(relief="groove")
Frame1.config(width="340", height="250")
Frame1.pack(side="left",anchor ="w")



#Creación y configuración del frame 2, el cual tiene el cuadro de texto para las acciones realizadas en el restaurante
Frame2=Frame()
Frame2.config(bg="Green")
Frame2.config(bd=10)
Frame2.config(relief="groove")
Frame2.config(width="450", height="650")
Frame2.pack(side="right", anchor="e")


#Texto de las ventanas del Frame de información
Label(Frame1,text="Ingrese las cantidades correspondientes",bg="Red", font=("Imprint MT Shadow",12)).place(x=10,y=10)
Label(Frame1,text="Numero de Meseros: ", bg="Red").place(x=10,y=35)
Label(Frame1,text="Numero de Mesas: ", bg="Red").place(x=10,y=65)
Label(Frame1,text="Numero de Chefs:", bg="Red").place(x=10,y=95)
Label(Frame1,text="Numero de Clientes", bg="Red").place(x=10,y=125)
#Cuadros de texto para las entradas de los datos incluyendo las variables en las que serán guardados cada valor.
Entry(Frame1,textvariable=meserosSTR).place(x=125,y=35)
Entry(Frame1,textvariable=mesasSTR).place(x=125,y=65)
Entry(Frame1,textvariable=chefsSTR).place(x=125,y=95)
Entry(Frame1,textvariable=clientesSTR).place(x=125,y=125)

"""Boton de envio de datos"""
Button(Frame1,text="Envio",width=7,command=lambda:envioDatos()).place(x=100,y=155)

#Cuadro de texto del frame 2, el cual tiene la información que registran los procesos
Label(Frame2,text="Registro de actividades", bg="Green", font=("Imprint MT Shadow",12)).grid(row=0,column=0)
action=Text(Frame2,width=50,height=20)
action.grid(row=1,column=0,padx=10,pady=10)
#Barra de Scroll para el cuadro de texto del registro de la información, esto para mejor manejo de la visualización
scrollVert=Scrollbar(Frame2,command=action.yview)
scrollVert.grid(row=1,column=1,sticky="nsew")
action.config(yscrollcommand=scrollVert.set)



#Funcion del boton que obtendrá los datos y los guardará en los datos globales

def envioDatos():
    global num_clientes, num_chefs, num_mesas, num_meseros, chefs, meseros, mesas
    action.delete('1.0',END)
    

    try:
        num_meseros=int(meserosSTR.get())
        num_mesas=int(mesasSTR.get())
        num_chefs=int(chefsSTR.get())
        num_clientes=int(clientesSTR.get())
        chefs = threading.Semaphore(num_chefs)
        meseros = threading.Semaphore(num_meseros)
        mesas = threading.Semaphore(num_mesas)
    except ValueError:
        action.insert(INSERT,"Valores incorrectos\n")
    if(num_meseros>0 and num_mesas>0 and num_chefs>0 and num_clientes>0):
        action.insert(INSERT,"ESTADO DEL RESTAURANTE\n")
        action.insert(INSERT,"\tNumero meseros: {} \n".format(str(meserosSTR.get())))
        action.insert(INSERT,"\tNumero mesas: {} \n".format(str(mesasSTR.get())))
        action.insert(INSERT,"\tNumero chefs: {} \n".format(str(chefsSTR.get())))
        action.insert(INSERT,"\tNumero clientes: {} \n".format(str(clientesSTR.get())))
        restaurante = Restaurante(num_meseros, num_chefs, num_clientes)

    else:
        action.insert(INSERT,"Valores incorrectos\n")

   



#######################################################################
#Código de las entidades del restaurante
###################################################################### 

class Cliente:
    def __init__(self, id_cliente, num_invitados):
        self.id_cliente = id_cliente
        self.num_invitados = num_invitados
        self.lista_invitados = []
        self.esperarComida = True
        #usaremos una barrera para que todos elijan su platillo
        self.cuenta_orden = 0
        self.mutex_orden = threading.Semaphore(1)
        self.barrera_orden = threading.Semaphore(0)
        #usaremos una barrera para que todos terminen de comer
        self.cuenta_comer = 0
        self.mutex_comer = threading.Semaphore(1)
        self.barrera_comer = threading.Semaphore(0)
        self.esperarMesa()

    def esperarMesa(self):
        global mesas, mutex_fila_espera, clientesEnEspera
        #se adquiere una mesa, cuando la adquiere se saca de la lista
        mesas.acquire()
        mutex_fila_espera.acquire()
        clientesEnEspera.pop(0)
        mutex_fila_espera.release()
        
        #print("Cliente {} esta listo".format(self.id_cliente))
        self.llamarMesero("mesa")
        self.obtenerMesa()
        self.llamarMesero("menu")
        self.leerMenuYOrdenar()
        self.llamarMesero("orden")
        while self.esperarComida == True:
            action.insert(INSERT,"Cliente {} esperando nuestra orden\n".format(self.id_cliente))
            
        self.comer()
        self.llamarMesero("cuenta")
        self.irse()

        mesas.release()
    
    #Acciones de interaccion del cliente con los invitados y al mesero
    def llamarInvitado(self,i):
        return threading.Thread(target = Invitado, args=[self, i]).start()

    def llamarMesero(self, peticion):
        global meserosDisponibles, meseros, mutex_meseros_disp
        action.insert(INSERT,"Cliente {} tiene una petición\n".format(self.id_cliente))

        #se pide un mesero, se saca de la lista de disponibles, se le da la peticion
        #al completar la acción el mesero regresa a estar disponible
        meseros.acquire()
        mutex_meseros_disp.acquire()
        mesero = meserosDisponibles.pop(0)
        mutex_meseros_disp.release()
        mesero.activar(peticion, self.id_cliente, self)
        meseros.release()

    def obtenerMesa(self):
        action.insert(INSERT,"<------Cliente {} consigue una mesa para {} personas\n".format(self.id_cliente,self.num_invitados+1))
        
    def leerMenu(self):
        action.insert(INSERT,"Cliente {} está escogiendo mi platillo\n".format(self.id_cliente))
        
        espera = random.randrange(1,5)
        for i in range(espera):
            pass

    def decidirOrden(self):
        self.mutex_orden.acquire()
        action.insert(INSERT,"Cliente {} decidío su orden\n".format(self.id_cliente))
        self.cuenta_orden += 1
        self.mutex_orden.release()


    def leerMenuYOrdenar(self):
        self.leerMenu()
        self.decidirOrden()
        acabar = True
        hilos = self.num_invitados + 1
        #aqui mandaremos a llamar a los invitados del cliente
        for i in range(self.num_invitados):
            self.llamarInvitado(i)
        #Barrera para esperar a que todos esten listos para ordenar
        while acabar:
            if self.cuenta_orden == hilos:
                self.barrera_orden.release()
                acabar = False
            
        action.insert(INSERT,"Todos en la mesa del cliente {} estan listos para ordenar\n".format(self.id_cliente))
        self.mutex_orden.acquire()
        self.mutex_orden.release()


    def comer(self):
        # + 1
        hilos = self.num_invitados
        acabar = True
        espera = random.randrange(1,5)
        for i in range(espera):
            pass
        action.insert(INSERT,"Cliente {} ha terminado de comer\n".format(self.id_cliente))
        
        #Hagamos que los invitados coman tambien
        for i in self.lista_invitados:
            i.comer()
        #barrera pa no ser descortes y esperar a que todos terminen de comer
        while acabar:
            if self.cuenta_comer == hilos:
                self.barrera_comer.release()
                acabar = False
        self.barrera_comer.acquire()
        self.barrera_comer.release()

        action.insert(INSERT,"Todos en la mesa del cliente {} han terminado de comer\n".format(self.id_cliente))
        self.mutex_comer.acquire()
        self.mutex_comer.release()

    def irse(self):
        action.insert(INSERT,"----->Cliente {} y sus {} invitados han decidido irse\n".format(self.id_cliente,self.num_invitados))

#Clase para los hilos que se encuentran enlazados con el cliente
class Invitado:
    def __init__(self,cliente,id_invitado):
        self.cliente = cliente
        self.id_invitado = id_invitado
        self.leerMenu()
        self.decidirOrden()
        
    #Acciones que realiza el invitado, siendo parecidas al del cliente
    def leerMenu(self):
        action.insert(INSERT,"El invitado {} del cliente {} leé el menu\n".format(self.id_invitado,self.cliente.id_cliente))
        
        espera = random.randrange(1,5)
        for i in range(espera):
            pass

    def decidirOrden(self):
        self.cliente.mutex_orden.acquire()
        action.insert(INSERT,"El invitado {} del cliente {} ha elegido su platillo\n".format(self.id_invitado,self.cliente.id_cliente))
        
        #tiempo espera
        self.cliente.cuenta_orden += 1
        self.cliente.mutex_orden.release()
        self.cliente.lista_invitados.append(self)

    def comer(self):
        #t espera
        self.cliente.mutex_comer.acquire()
        action.insert(INSERT,"El invitado {} del cliente {} ha terminado de comer\n".format(self.id_invitado,self.cliente.id_cliente))
        
        #*
        self.cliente.cuenta_comer += 1
        self.cliente.mutex_comer.release()

#Clase para los hilos que actuarán como meseros
class Mesero:
    def __init__(self, id_mesero):
        self.id_mesero = id_mesero
        self.descansar = threading.Semaphore(0)
        #*
        self.enlistar()

    def enlistar(self):
        global meserosDisponibles
        mutex_meseros_disp.acquire()
        meserosDisponibles.append(self)
        mutex_meseros_disp.release()

    #Dependiendo del cliente, el mesero realizará diferentes acciones
    def activar(self, peticion, id_cliente, cliente):
        global mutex_meseros_disp, meserosDisponibles
        #self.descansar.release()

        if peticion == "mesa":
             self.llevarMesa(id_cliente)
        elif peticion == "menu":
             self.mostrarMenu(id_cliente)
        elif peticion == "orden":
             self.llevarOrdenAChef(id_cliente, cliente)
        elif peticion == "ordenLista":
             self.llevarOrdenAMesa(id_cliente, cliente)
        elif peticion == "cuenta":
             self.traerCuenta(id_cliente)

        action.insert(INSERT,"Mesero {} se encuentra libre\n".format(self.id_mesero))
        self.enlistar()

    def llevarMesa(self, id_cliente):
        action.insert(INSERT,"Mesero {} lleva a Cliente {} a su mesa\n".format(self.id_mesero,id_cliente))
        
    def mostrarMenu(self, id_cliente):
        action.insert(INSERT,"Mesero {} le ha dado los Menus a todos en la mesa del cliente {} \n".format(self.id_mesero,id_cliente))
        
    def llevarOrdenAChef(self, id_cliente, cliente):
        global chefsDisponibles, chefs, mutex_chefs_disp
        action.insert(INSERT,"Mesero {} llevó la orden del cliente {} a preparar\n".format(self.id_mesero,id_cliente))
        

        #se pide un chef, se saca de la lista de disponibles
        #al completar la acción el chef regresa a estar disponible
        chefs.acquire()
        mutex_chefs_disp.acquire()
        chef = chefsDisponibles.pop(0)
        mutex_chefs_disp.release()
        chef.cocinar(cliente)
        chefs.release()

    def llevarOrdenAMesa(self, id_cliente, cliente):
        action.insert(INSERT,"Mesero {} llevó la orden lista del cliente {} \n".format(self.id_mesero,id_cliente))
        cliente.esperarComida = False

    def traerCuenta(self, id_cliente):
        action.insert(INSERT,"Mesero {} llevó la cuenta en la mesa del cliente {} \n".format(self.id_mesero,id_cliente))

#Entidad para los hilos que actuan como chefs
class Chef:
    def __init__(self, id_chef):
        self.id_chef = id_chef
        self.enlistar()
    #Funcion para que el chef desocupado entre a la lista de chefs disponibles
    def enlistar(self):
        global chefsDisponibles
        mutex_chefs_disp.acquire()
        chefsDisponibles.append(self)
        mutex_chefs_disp.release()
    #Funcion para la preparación del la orden del chef con una espera para terminar el platillo
    def cocinar(self, cliente):
        action.insert(INSERT,"Chef {} preparó la orden del cliente {} \n".format(self.id_chef,cliente.id_cliente))
        espera = random.randrange(1,5)
        for i in range(espera):
            pass
        action.insert(INSERT,"Chef {} terminó la orden del cliente {} \n".format(self.id_chef,cliente.id_cliente))
        
        #busquemos un mesero que lleve la orden
        meseros.acquire()
        mutex_meseros_disp.acquire()
        mesero = meserosDisponibles.pop(0)
        mutex_meseros_disp.release()
        mesero.activar("ordenLista", cliente.id_cliente, cliente)
        meseros.release()

        action.insert(INSERT,"Chef {} está libre \n".format(self.id_chef))
        self.enlistar()


#Entidad del restaurante, utilizado para la inicializacion de las variables y el manejo del proyecto
class Restaurante:
    def __init__(self, num_meseros, num_chefs, num_clientes):
        for i in range(num_chefs):
            threading.Thread(target= Chef, args=[i]).start()
        

        for i in range(num_meseros):
            threading.Thread(target= Mesero, args=[i]).start()
       
        for i in range(num_clientes):
            num_invitados = random.randrange(1,5)
            mutex_fila_espera.acquire()
            clientesEnEspera.append( threading.Thread(target= Cliente, args=[i, num_invitados]).start())
            mutex_fila_espera.release()
        if(len(meserosDisponibles)==num_meseros and len(clientesEnEspera)==0 and len(chefsDisponibles)==num_chefs):
            action.insert(END,"El restaurante ha cerrado sus puertas. \nHASTA LUEGO :)\n")
            print("El restaurante ha cerrado sus puertas. \nHASTA LUEGO :)\n")



#Función para la aparición del la pantalla de la interfaz
raiz.mainloop()

