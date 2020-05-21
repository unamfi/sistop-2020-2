import os
import time
import tkinter as tk
from tkinter import ttk 
carp='/fiunamfs'

def inicio():
    print("********************************************************\n**********************ADVERTENCIA***********************\n********************************************************\nLos comandos que seran utilizados requieren de que se \nejecuten como sudo o su, por ello se necesitara la \nejecucion como sudo python3 FiUnamFs.py o brindar de \nmanera manual el permiso, cada que se le solicite")
    #le damos el formato al disco ext4
    os.system('sudo mkfs -t ext4 ./fiunamfs.img')
    #creamos la carpeta en la que se montara el disco
    os.system('sudo mkdir /mnt'+carp)
    print('Carpeta para montar creada')
    #Montado del disco en la carpeta creada
    os.system('sudo mount -r -t auto -o loop ./fiunamfs.img /mnt'+carp)
    print('Disco montado en /mnt'+carp)
    #Comprobacion del montado del disco
    os.system('df -hT')
    
"""FUNCIONALIDADES """
def nuevo(nombre,ext):
    os.system('touch '+nombre+ext)

def cierra():
    
    
def n():
    nuevo = tk.Toplevel() 
    nuevo.title('Crear nuevo archivo')
    ins=tk.Label(text='Por favor ingrese el nombre del archivo y seleccione la extensión deseada')
    ins.grid(column=0,row=0)
    nombre=tk.Entry(nuevo)
    nombre.grid(column=0,row=1)
    ext=ttk.Combobox(nuevo, width=27,textvariable='Elija uno')
    ext['values']=('.com','.html','.docx','.pptx','.jpg','.png','.exe','.svg','.ico')
    ext.grid(column=2,row=1)
    boton=(nuevo,text='Aceptar',command=nuevo(nombre.get(),ext.current()))
    nuevo.mainloop() 

def o():
    pass

def rm():
    pass



'''Crearemos la interfaz grafica con tkinter'''
def gui():    
    vent_princip=tk.Tk()
#    imgicon = tk.PhotoImage(file=os.path.join('favicon.ico'))
#    vent_princip.tk.call('wm', 'iconbitmap', vent_princip._w, imgicon)  
#    vent_princip.iconbitmap(os.path.join('favicon.ico'))
    vent_princip.geometry('500x500')
    vent_princip.title('Sistema de Archivos Fi-UNAM')    
    os.system('cd /mnt/fiunamfs')
    menu = tk.Menu(vent_princip)
    vent_princip.config(menu=menu)
    filemenu = tk.Menu(menu) 
    menu.add_cascade(label='Archivo', menu=filemenu) 
    filemenu.add_command(label='Nuevo',command=n) 
    filemenu.add_command(label='Abrir',command=o)
    filemenu.add_command(label='Eliminar',command=rm)
    filemenu.add_separator() 
    filemenu.add_command(label='Salir', command=vent_princip.quit) 
    helpmenu = tk.Menu() 
    menu.add_cascade(label='Ayuda', menu=helpmenu) 
    helpmenu.add_command(label='Acerca de ') 
    #  
    label1=tk.Label(vent_princip,text='Listado de archivos')
    label1.grid(column=0,row=1)
    #
    lista = os.listdir('/mnt'+carp)
    arch=tk.Listbox(vent_princip)
    #arch.pack()
    for i in lista:
        arch.insert(tk.END, i)
    arch.grid(column=0,row=2) 
    vent_princip.mainloop()

def fin():
    
    '''¡¡¡A LEVANTAR LOS JUGUETES!!!'''
    print('Desmontando el disco')
    os.system('sudo umount /mnt'+carp)
    print('Eliminacion de la carpeta')
    os.system('sudo rmdir /mnt'+carp)
    print('Carpeta eliminada')

if __name__=="__main__":
    inicio()
    gui()
    fin()

