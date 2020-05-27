'''
 * @Authors: Fernando Arturo Medina Molina, Sergio Osorio Sánchez
 * @Version: 1.0
 * @Copyleft:
 * 1.-Usarla sin ninguna limitación.
 * 2.-Libertad de estudio (ver cómo está hecho el trabajo).
 * 3.-(re)distribuir cuantas copias desee.
 * 4.-Modificarla de la manera que crea conveniente.
 * @Description: Gracias a lo visto en las clases de teoría de Sistemas Operativos se pretende crear un 'micro-Sistema de archivos' el cual contenga las operaciones simples de Importar, Exportar, Desfragmentar y Eliminar archivos en un Disco o archivo .img proporcionado por el profesor, en este caso será el archivo fiunamfs.py .
 * @Referencias:  
 * °https://github.com/gwolf/sistop-2019-2/blob/master/proyectos/3/FranciscoRodrigo-SanchezBeatriz/fsm.py
 * °https://github.com/unamfi/sistop-2020-1/blob/master/proyectos/3/RosalesRicardo/main.py
 * @Contact: fernando170@comunidad.unam.mx
'''

import os
import sys
import errno
import time
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from tkinter import filedialog
from fifs import FIFS
import sys
fs = FIFS()

def inicio():
    '''
    Rutina inicial del programa, al ejecutarse desde una terminal, desplegará la información necesaria para que el programa sea ejecutado de manera correcta, ya que son necesarios los permisos de administrador para realizar las operaciones escenciales.
    Nota.: IMPORTANTE, si el plrograma no esejecutado como administrador o se le brindan los permisos pertinentes no se asegura la correcta ejecución del programa.
    '''
    print("********************************************************\n**********************ADVERTENCIA***********************\n********************************************************\nLos comandos que seran utilizados requieren de que se \nejecuten como sudo o su, por ello se necesitará la \nejecución de la forma 'sudo python3 FiUnamFs.py' o brindar de \nmanera manual el permiso, cada que se le solicite")
    
#*************************FUNCIONES*****************************
def cierra():
    '''
    Cerraremos el programa 
    '''
    fin()
	

def desfragmentar():
    '''
   Con la funcionalidad desfragmentar lograremos que el volúmen sea desgragmentado gracias a la función defrag() encontrada en el archivo fifs.py y utilizamos dentro de nuestro programa, invocándolo con el comando Desfragmentar ubicado en el menú principal.
    '''
    fs.defrag()
    tk.messagebox.showinfo(title='Desfragmentado exitoso',message='EL volumen ha sido desfragmentado exitosamente')


def rm():
    '''
    Gracias a la función 'rm' invocada en el menú por el comando eliminar, despliegaremos una ventana la cual a través de una entrada de texto podremos especificar los inodos que deseamos perder referencia, o eliminar los archivos que especifiquemos, indicando uno por uno el nombre y extensión del archivo deseado. Una vez realizada la eliminación se despliegará un mensaje informativo confirmando dicha operación.
    '''
    eliminar = tk.Toplevel()
    eliminar.title('ELiminar archivo')
    ins=tk.Label(eliminar,text='Por favor ingrese el nombre del archivo que desea eliminar (incluyendo su extensión).').grid(column=0,row=0)
    nombre=tk.Entry(eliminar)
    nombre.grid(column=0,row=1)
    def elimina():
        if (str(nombre.get())==''):
            tk.messagebox.showinfo(title='Archivo no eliminado',message='Por favor indique el nombre y extensión de archivo que desea eliminar.')
        else:
            fs.rm(str(nombre.get()))
            tk.messagebox.showinfo(title='Archivo eliminado',message='El archvo '+str(nombre.get())+' ha sido eliminado')

    tk.Button(eliminar,text='Aceptar',command=elimina).grid(column=0,row=2)
    eliminar.mainloop()

def copyin():
    '''
   Con la funcionalidad de copyin() podemos realizar la operación de transferencia de un archivo local al disco con el que se está operando, la función desplegará un selector de archivos del sistema local, seleccionar el deseado, har click en abrir y el archivo será insertado en el disco.
    '''
    nuevo=tk.Toplevel()
    nuevo.title("Copiar archivo en el sistema")
    file_c = filedialog.askopenfilename()
    fs.cpin(str(file_c))
    tk.messagebox.showinfo(title='Archivo copiado',message='El archvo '+file_c+' ha sido copiado en el sistema de archivos')
    
def ajustar_print(entrada):
    '''
    Con ésta función pretendemos ajustar la cadena de caracteres devuelta por la función ls() la cual nos permite mostrar de una manera más organizada los archivos que son listados en el list box, retornará una cadena de caracteres con un formato específico
    :param: entrada. Será la cadena de caractres a la que se le dará formato. Type: string.
    :return: nuevaCadena. Es la cadena que retornamos con un formato específico para ser desplegada en el listbox. Type: String.
    '''
    nuevaCadena = ''
    if len(entrada[0])<15:
        for i in range(14):
            if len(entrada[0])==i:
                espacios=entrada[0]
                for j in range(15-i):
                    espacios=espacios+' '
                nuevaCadena=nuevaCadena+espacios
    else:
        nuevaCadena=nuevaCadena+entrada[0]                           
    nuevaCadena+='   '
    if len(entrada[1])<10:
        for i in range(6):
            if len(entrada[1])==i:
                espacios=entrada[1]
                for j in range(7-i):
                    espacios=espacios+' '
                nuevaCadena=nuevaCadena+espacios
    else:
        nuevaCadena=nuevaCadena+entrada[1]
    
    if len(entrada[2])<=9:
        for i in range(8):
            if len(entrada[2])==i:
                espacios=entrada[2]
                for j in range(9-i):
                    espacios=espacios+' '
                nuevaCadena=nuevaCadena+espacios
    else:
        nuevaCadena=nuevaCadena+entrada[2]
    nuevaCadena+='  '
    if len(entrada[3])<7:
        for i in range(6):
            if len(entrada[3])==i:
                espacios=entrada[3]
                for j in range(7-i):
                    espacios=espacios+' '
                nuevaCadena=nuevaCadena+espacios
    else:
        nuevaCadena=nuevaCadena+entrada[3]
    nuevaCadena+='  '
    if len(entrada[4])<7:
        for i in range(6):
            if len(entrada[4])==i:
                espacios=entrada[4]
                for j in range(7-i):
                    espacios=espacios+' '
                nuevaCadena=nuevaCadena+espacios
    else:
        nuevaCadena=nuevaCadena+entrada[4]
    if len(entrada[5])<7:
        for i in range(6):
            if len(entrada[5])==i:
                espacios=entrada[5]
                for j in range(7-i):
                    espacios=espacios+' '
                nuevaCadena=nuevaCadena+espacios
    else:
        nuevaCadena=nuevaCadena+entrada[5]
    nuevaCadena+='   '
    if len(entrada[6])<7:
        for i in range(6):
            if len(entrada[6])==i:
                espacios=entrada[6]
                for j in range(7-i):
                    espacios=espacios+' '
                nuevaCadena=nuevaCadena+espacios
    else:
        nuevaCadena=nuevaCadena+entrada[6]
    return(nuevaCadena)
def copyout():
    '''
    Con coupyout() podremos importar al sistema local los archivos que se deseen y se encuentren dentro del disco. La función desiplegará una ventana en la cual solo ingresará en la casilla de texto, el nombre del archivo deseado (junto con su extensión), al hacer click en el botón de aceptar se abrirá otra ventana en la cual tendrá que seleccionar el nombre de la carpeta en la que será alojado el archivo. Finalmente se mostrará un mensaje informativo confirmando la operación.
    '''
    nuevo=tk.Toplevel()
    nuevo.title("Copiar archivo hacia el sistema local")
    ins=tk.Label(nuevo,text='Por favor ingrese el nombre del archivo que desea copiar a su sistema local de archivos (incluyendo su extensión).').grid(column=0,row=0)
    nombre=tk.Entry(nuevo)
    nombre.grid(column=0,row=1)
    def elimina():
        if (str(nombre.get())==''):
            tk.messagebox.showinfo(title='Archivo no copiado',message='Por favor indique el nombre y extensión de archivo que desea copiar.')
        else:
            file_co = filedialog.askdirectory()
            tk.messagebox.showinfo(title='Archivo copiado',message=fs.cpout(str(nombre.get()),file_co))
            

    tk.Button(nuevo,text='Aceptar',command=elimina).grid(column=0,row=2)
    nuevo.mainloop()
 
def ayuda():
    '''
    Con la función ayuda podrá acceder a esta documentación la cual será desplegada a través de su navegador. ésta se encuentra en un archivo .html
    '''
    aiura = tk.Toplevel()
    aiura.title('Documentación')
    a= open("./Documentacion.txt")
    aiura.geometry('300x300')
    T = tk.Text(aiura, height=250, width=300)
    T.pack()
    T.insert(1.0, a.read())
    aiura.mainloop()
#*************Crearemos la interfaz grafica con tkinter***********
def gui():
    '''
    gui() será la funcionalidad más importante, ya que es la ventana principal conteniente de todas las funcionalidades contenientes en el sistema de archivos, así mismo, contiene la función que despliega ésta documentación.
    '''    
    vent_princip=tk.Tk()
    vent_princip.geometry('544x400')
    vent_princip.title('Sistema de Archivos Fi-UNAM')   
    menu = tk.Menu(vent_princip)
    vent_princip.config(menu=menu)
    filemenu = tk.Menu(menu)
    nuevo_menu=tk.Menu(filemenu)
    menu.add_cascade(label='Archivo', menu=filemenu)
    filemenu.add_command(label='Exportar de el sistema',command=copyout)
    filemenu.add_command(label='Importar hacia el sistema',command=copyin)
    filemenu.add_command(label='Eliminar',command=rm)
    filemenu.add_command(label='Desfragmentar',command=desfragmentar)
    filemenu.add_command(label='Eliminar Archivo',command=rm)
    filemenu.add_separator() 
    filemenu.add_command(label='Salir', command=vent_princip.quit) 
    helpmenu = tk.Menu() 
    menu.add_cascade(label='Ayuda', menu=helpmenu) 
    helpmenu.add_command(label='Acerca de ', command=ayuda)
    menu.add_command(label='Actualizar',command=gui)
    #  
    label1=tk.Label(vent_princip,text='Listado de archivos')
    label1.grid(column=0,row=1)
    #
    lista=fs.ls()
    arch=tk.Listbox(vent_princip,height=50,width=75)
    desc=tk.Label(vent_princip,text='NOMBRE      |  INICIO  |   FIN   |  MES  |  DIA  |  AÑO  |  hora:min:seg').grid(column=0,row=2)

    for i in lista:
        trozos=i.split()
        arch.insert(tk.END,ajustar_print(trozos)) 
    arch.grid(column=0,row=3) 
    vent_princip.mainloop()

#*********MAIN********
if __name__=="__main__":
    inicio()
    gui()
