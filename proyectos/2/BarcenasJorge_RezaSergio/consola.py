from tkinter import *
raiz=Tk()

meseros=StringVar()
mesas=StringVar()
chefs=StringVar()
clientes=StringVar()
num_meseros=0
num_mesas=0
num_chefs=0
num_clientes=0
def envioDatos():

    print("Numero meseros"+str(meseros.get()))
    print("Numero mesas"+str(mesas.get()))
    print("Numero chefs" +str(chefs.get()))
    print("Numero clientes"+str(clientes.get()))

    try:
    	num_meseros=int(meseros.get())
    	num_mesas=int(mesas.get())
    	num_chefs=int(chefs.get())
    	num_clientes=int(clientes.get())
    except ValueError:
    	print("Valores incorrectos")


"""Parametros iniciales para la ventana"""
raiz.title("Le Restaurante")
raiz.resizable(False, False)
raiz.geometry("650x450")
raiz.config(bg="beige")

Label(raiz,text="Bienvenido al \"Le Restaurant\"",bg="White",font=("Imprint MT Shadow",20)).place(x=175,y=30)

#Creación de frame para la ventana
Frame1=Frame()
Frame1.pack(side="left",anchor ="w")
Frame1.config(bg="Red")
Frame1.config(bd=10)
Frame1.config(relief="groove")
Frame1.config(width="320", height="250")

Frame2=Frame()
Frame2.pack(side="right", anchor="e")
Frame2.config(bg="Green")
Frame2.config(bd=10)
Frame2.config(relief="groove")
Frame2.config(width="350", height="250")



#Texto de las ventanas del Frame de información
Label(Frame1,text="Ingrese las cantidades correspondientes",bg="Red", font=("Imprint MT Shadow",12)).place(x=10,y=10)
Label(Frame1,text="Numero de Meseros: ", bg="Red").place(x=10,y=35)
Label(Frame1,text="Numero de Mesas: ", bg="Red").place(x=10,y=65)
Label(Frame1,text="Numero de Chefs:", bg="Red").place(x=10,y=95)
Label(Frame1,text="Numero de Clientes", bg="Red").place(x=10,y=125)
Entry(Frame1,textvariable=meseros).place(x=125,y=35)
Entry(Frame1,textvariable=mesas).place(x=125,y=65)
Entry(Frame1,textvariable=chefs).place(x=125,y=95)
Entry(Frame1,textvariable=clientes).place(x=125,y=125)

"""Boton de envio de datos"""
Button(Frame1,text="Envio",width=7,command=lambda:envioDatos()).place(x=100,y=155)



Label(Frame2,text="Registro de actividades", bg="Green", font=("Imprint MT Shadow",12)).grid(row=0,column=0)
action=Text(Frame2,width=30,height=12)
action.grid(row=1,column=0,padx=10,pady=10)

scrollVert=Scrollbar(Frame2,command=action.yview)
scrollVert.grid(row=1,column=1,sticky="nsew")
action.config(yscrollcommand=scrollVert.set)

raiz.mainloop()