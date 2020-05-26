import os
import sys
import errno
import time
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
carp='/fiunamfs'

def inicio():
    print("********************************************************\n**********************ADVERTENCIA***********************\n********************************************************\nLos comandos que seran utilizados requieren de que se \nejecuten como sudo o su, por ello se necesitara la \nejecucion como sudo python3 FiUnamFs.py o brindar de \nmanera manual el permiso, cada que se le solicite")
    #le damos el formato al disco ext4
    os.system('sudo mkfs -t fat ./fiunamfs.img')
    #creamos la carpeta en la que se montara el disco
    os.system('sudo mkdir /mnt'+carp)
    print('Carpeta para montar creada')
    #Montado del disco en la carpeta creada
    os.system('sudo mount ./fiunamfs.img /mnt'+carp)
    print('Disco montado en /mnt'+carp)
    #Comprobacion del montado del discopython
    os.system('df -hT')
    
"""FUNCIONALIDADES """
def cierra():
	
	'''
	Con la función cierra, cerraremos por completo el programa, corriendo la secuencia fin(), no será necesario incluir parámetro alguno
        '''
	fin()
	pass


def nc():
    nuevo = tk.Toplevel()
    nuevo.title('Crear nueva carpeta')
    la=tk.Label(nuevo,text='Por favor ingrese el nombre de la carpeta a crear')
    la.grid(column=0,row=0)
    nombrec=tk.Entry(nuevo)
    nombrec.grid(column=0,row=1)
    def nuevac():
        '''
        Con ésta función crearemos en el disco una carpeta con el nombre específicado en el parámetro nom, en dado caso de que no se pueda generar la carpeta se informará al usuario a través de una ventana.
        :param nombre: El nombre que se le dará a la nueva carpeta. type: String
        '''
        try:
            os.mkdir('/mnt'+carp+str(nombrec.get()))
            tk.messagebox.showinfo(title='Carpeta creada',message='La carpeta '+str(nombre.get())+' ha sido creada')
        except OSError as e:
            if e.errno == errno.EEXIST:
                print('Directory not created.')
            else:
                raise
                tk.messagebox.showinfo(title='Carpeta no creada',message='Fallo al intentar crear carpeta nueva, es posible que ya exista una con el mismo nombre.')
                print(sys.exc_info()[0])
                nuevo.destroy()
    
    boton2=tk.Button(nuevo,text='Aceptar',command=nuevac)
    boton2.grid(column=0,row=3)
    nuevo.mainloop()
    '''
    Con la función nc se pretende desplegar una pantalla en la cual ingresaremos el nombre de la carpeta que será creada a través de la función nuevac.	
    '''


def na():
    '''Con la función n crearemos un nuevo archivo con la '''
    nueva = tk.Toplevel()
    nueva.title('Crear nuevo archivo')
    ins=tk.Label(nueva,text='Por favor ingrese el nombre del archivo y seleccione la extensión deseada').grid(column=0,row=0)
    nombre=tk.Entry(nueva)
    nombre.grid(column=0,row=1)
    ext=ttk.Combobox(nueva, width=27,text='Elija uno')
    ext['values']=('com','html','docx','pptx','jpg','png','exe','svg','ico')
    ext.grid(column=2,row=1)
    print('creación de archivo')
    def nuevoa():
        '''
        Con la función nuevoa se pretende crear el archivo con la extensión deseada por el usuario, ya sea que el la ingrese manualmente o utilizando el combobox proporcionado con las opciones más comunes, el nombre estará dado por el parámetro nombre y la extensión por el parametro ext
        :param nombre: Nombre del archivo que vamos a crear. type: String
        :param ext: Nombre de la extensión que tendrá el archivo, puede ser nulo. type: String
        '''
        if(ext==''or ext==None or ext==-1):
                open(str(nombre.get()),'w')
                tk.messagebox.showinfo(title='Archivo creado',message='El archvo '+str(nombre.get())+' ha sido creado')
        else:
                open(str(nombre.get())+'.'+str(ext.current()),'w')
                tk.messagebox.showinfo(title='Archivo creado',message='El archvo '+str(nombre.get())+'.'+str(ext.current())+' ha sido creado')
    tk.Button(nueva,text='Aceptar',command=nuevoa).grid(column=0,row=2)
    nueva.mainloop()

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
    vent_princip.geometry('300x300')
    vent_princip.title('Sistema de Archivos Fi-UNAM')    
    os.system('cd /mnt/fiunamfs')
    menu = tk.Menu(vent_princip)
    vent_princip.config(menu=menu)
    filemenu = tk.Menu(menu)
    nuevo_menu=tk.Menu(filemenu)
    nuevo_menu.add_command(label='Archivo',command=na)
    nuevo_menu.add_command(label='Carpeta',command=nc)
    menu.add_cascade(label='Archivo', menu=filemenu)
    filemenu.add_cascade(label='Nuevo',menu=nuevo_menu)
    
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
    arch=tk.Listbox(vent_princip,width=40)

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

