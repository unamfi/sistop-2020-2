import os
import sys
import errno
import time
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from fifs import FIFS
import sys
fs = FIFS()

def inicio():
    print("********************************************************\n**********************ADVERTENCIA***********************\n********************************************************\nLos comandos que seran utilizados requieren de que se \nejecuten como sudo o su, por ello se necesitará la \nejecución de la forma 'sudo python3 FiUnamFs.py' o brindar de \nmanera manual el permiso, cada que se le solicite")
    
"""FUNCIONALIDADES """
def oF():
    nuevo=tk.Toplevel()
    nuevo.title("Abrir imagen")
    file_img = filedialog.askopenfilename()
    FS = FileSystem(file_img)
    
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
                open('/mnt'+carp+str(nombre.get()),'w')
                tk.messagebox.showinfo(title='Archivo creado',message='El archvo '+str(nombre.get())+' ha sido creado')
        else:
                open('/mnt'+carp+str(nombre.get())+'.'+str(ext.current()),'w')
                tk.messagebox.showinfo(title='Archivo creado',message='El archvo '+str(nombre.get())+'.'+str(ext.current())+' ha sido creado')
    tk.Button(nueva,text='Aceptar',command=nuevoa).grid(column=0,row=2)
    nueva.mainloop()

def o():
    pass

def rm():
    eliminar = tk.Toplevel()
    eliminar.title('Crear nuevo archivo')
    ins=tk.Label(eliminar,text='Por favor ingrese el nombre del archivo y seleccione la extensión deseada').grid(column=0,row=0)
    nombre=tk.Entry(eliminar)
    nombre.grid(column=0,row=1)
    ext=ttk.Combobox(eliminar, width=27,text='Elija uno')
    ext['values']=('com','html','docx','pptx','jpg','png','exe','svg','ico')
    ext.grid(column=2,row=1)
    print('creación de archivo')
    def elimina():
        fs.rm(str(nombre.get()))
        tk.messagebox.showinfo(title='Archivo eliminado',message='El archvo '+str(nombre.get())+' ha sido eliminado')

    tk.Button(eliminar,text='Aceptar',command=nuevoa).grid(column=0,row=2)
    eliminar.mainloop()


    pass



'''Crearemos la interfaz grafica con tkinter'''
def gui():    
    vent_princip=tk.Tk()
#    imgicon = tk.PhotoImage(file=os.path.join('favicon.ico'))
#    vent_princip.tk.call('wm', 'iconbitmap', vent_princip._w, imgicon)  
#    vent_princip.iconbitmap(os.path.join('favicon.ico'))
    vent_princip.geometry('350x350')
    vent_princip.title('Sistema de Archivos Fi-UNAM')   
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
    filemenu.add_command(label='Desfragmentar')
    filemenu.add_command(label='Abrir .img',command=oF)
    filemenu.add_command(label='Eliminar Archivo',command=rm)
    filemenu.add_separator() 
    filemenu.add_command(label='Salir', command=vent_princip.quit) 
    helpmenu = tk.Menu() 
    menu.add_cascade(label='Ayuda', menu=helpmenu) 
    helpmenu.add_command(label='Acerca de ') 
    #  
    label1=tk.Label(vent_princip,text='Listado de archivos')
    label1.grid(column=0,row=1)
    #
    lista=[]
    lista.append(fs.ls())
    arch=tk.Listbox(vent_princip,height=50,width=50)
    arch.insert(tk.END,'nombre    inicio    fin   mes   día    año    hora:min:seg')
    print('/********************************************\n'+str(lista))

    for i in lista:
        arch.insert(tk.END, i)
    arch.grid(column=0,row=2) 
    vent_princip.mainloop()


if __name__=="__main__":
    inicio()
    gui()

