import os
import time
import tkinter
carp='/fiunamfs'
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
#os.system('df -hT')
'''Crearemos la interfaz grafica con tkinter'''
vent_princip=tkinter.Tk()
#name = tkinter.tkFileDialog.askopenfilename(initialdir = curr_directory,title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
#print(name)
vent_princip.mainloop()
'''¡¡¡A LEVANTAR LOS JUGUETES!!!'''
print('Desmontando el disco')
os.system('sudo umount /mnt'+carp)
print('Eliminacion de la carpeta')
os.system('sudo rmdir /mnt'+carp)
print('Carpeta eliminada')

