# -*- coding: utf-8 -*-
"""
	Proyecto 3: Asignación de memoria en un sistema real
	Alumnos:
        Barcenas Avelas Jorge Octavio
        Reza Chavarria Sergio Gabriel
    Profesor:
        Gunnar Eyal Wolf Iszaevich

"""
#Interfaz gráfica
from tkinter import *
import os

###################################################################################
#Interfaz Gráfica
###################################################################################
#Creacion de ventana para salida
raiz=Tk()
PIB=StringVar()
num_PIB=0
#PArametros de ventana
raiz.title("Proyecto 3: Asignacion de memoria en un sistema real")
raiz.resizable(False, False)
raiz.geometry("1100x650")
raiz.config(bg="#b8c9ff")

#Parametros de frame que contiene la barra de texto para la seleccion del PIB
Frame1=Frame()
Frame1.config(bg='#6c80bf')
Frame1.config(bd=10)
Frame1.config(relief="groove")
Frame1.config(width="700", height="100")
Frame1.pack(side="top")
Label(Frame1,text="Ingrese PIB deseado: ", font=("Imprint MT Shadow",12)).grid(row=0,column=0)
Entry(Frame1,textvariable=PIB).grid(row=0,column=1)
Button(Frame1,text="Envio",width=7,command=lambda:envioDatos()).grid(row=0,column=2)

#Ventana que contiene la informacion del archivo
Frame2=Frame()
Frame2.config(bg='#6c80bf')
Frame2.config(bd=10)
Frame2.config(relief="groove")
Frame2.config(width="700", height="450")
Frame2.pack(side="bottom")
#Cuadro de texto del frame 1, el cual tiene la información del map
Label(Frame2,text="NEW MAP", font=("Imprint MT Shadow",12)).grid(row=0,column=0)
action=Text(Frame2, wrap=NONE,width=100,height=30)
action.grid(row=0,column=0,padx=10,pady=10)
#Barra de Scroll para el cuadro de texto del registro de la información, esto para mejor manejo de la visualización
scrollVert=Scrollbar(Frame2,command=action.yview)
scrollVert.grid(row=0,column=1,sticky="nsew")
action.config(yscrollcommand=scrollVert.set)
scrollHor=Scrollbar(Frame2,command=action.xview,orient='horizontal')
scrollHor.grid(row=1,column=0,sticky="nsew")
action.config(xscrollcommand=scrollHor.set)

#Etiquetas para el color de impresion en la ventana
action.tag_configure('color_uso',foreground='blue')
action.tag_configure('color_inicioP',foreground='green')
action.tag_configure('color_finP',foreground='green')
action.tag_configure('color_num_size',foreground='red')
action.tag_configure('color_num_pag',foreground='#7000ff')
action.tag_configure('color_permisos',foreground='#ff8f00')
action.tag_configure('color_mapeo',foreground='#ff00ff')




##Funcion para el envio del PIB 
def envioDatos():
	action.delete('1.0',END)
	try:
		num_PIB=int(PIB.get())
	except ValueError:
		action.insert(INSERT,"Valores incorrectos\n")
	if(num_PIB>0):
		action.insert(INSERT,"PIB: {}\n".format(str(num_PIB)))
		inicioMap(num_PIB)

	else:
		action.insert(INSERT,"Valores incorrectos\n")



#######################################################################
#Manejo de informacion
########################################################################



#Clase para el guardado de datos del archivo
class infoArchivos:
	#Clase con la obtencio de informacion, y calculos de size del archivo y cantidad de paginas
	def __init__(self,uso,pagina,permisos,mapeo):
		self.uso=uso
		paginaAUX=pagina.split("-")
		self.paginacompleta=pagina
		self.inicioPagina=paginaAUX[1]
		self.finPagina=paginaAUX[0]
		self.num_size=self.CalculoSIZEPag()
		self.num_pag=self.calculoPaginas()
		self.permisos=permisos
		self.mapeo=mapeo
	#Fomato de impresion de info
	def printInfo(self):
		return("|| {:7} || {:16} - {:16} || {:12} || {:12} || {:4} || {}\n".format(self.uso,self.inicioPagina,self.finPagina,self.num_size,self.num_pag,self.permisos,self.mapeo))
	
	"""
	def CalculoSize(self):
		self.size=self.size.replace("kB","")
		num_size=int(self.size)
		if((num_size/1024)>=1):
			if((num_size/1048576)>=1):
				return str((num_size/1048576))+" Gb"
			else:
				return str((num_size/1024))+" Mb"
		else:
			return str(num_size)+" kB"
			"""
	"""
	Metodo para la obtencion del size, siendo si tiene que ser 
	"""
	def CalculoSIZEPag(self):
		#Calculo de tamanio de archivo
		inipag=int(self.inicioPagina,16)
		finpag=int(self.finPagina,16)
		resta=int((inipag-finpag)/1024)
		#Dependiendo del tamanio se anexa Gb,Mb kB
		if((resta/1024)>=1):
			if((resta/1048576)>=1):
				return str((resta/1048576))+" Gb"
			else:
				return str((resta/1024))+" Mb"
		else:
			return str(resta)+" kB"

	#CAlculo de la cantidad de paginas a partir del tamanio
	#ESto depende del tamanio en kB
	def calculoPaginas(self):
		if "kB" in self.num_size:
			size=self.num_size.replace("kB","")
			num_size=float(size)
			num_size=int(num_size)
			#print(str(num_size)+"kB")
		elif "Mb" in self.num_size:
			size=self.num_size.replace("Mb","")
			num_size=float(size)
			num_size=num_size*1024
			num_size=int(num_size)
			#print(str(num_size)+"Mb")
		elif "Gb" in self.num_size:
			size=self.num_size.replace("Gb","")
			num_size=float(size)
			num_size=num_size*1024*1024
			num_size=int(num_size)
			#print(str(num_size)+"Gb")

		"""
		self.pag=self.pag.replace("kB","")
		num_pag=int(self.pag)
		"""
		num_pag=4
		#print(str(num_size/num_pag)+"\n")
		return str(int(num_size/num_pag))+" pags."



def inicioMap(num_PIB):
	#Parametros globales para obtencion de informacion del pib
	maps = 'cat /proc/' + str(num_PIB) + '/maps > maps'+str(num_PIB)+'.txt'
	smaps = 'cat /proc/' + str(num_PIB) + '/smaps > smaps'+str(num_PIB)+'txt'
	listaUso=['[heap]','[stack]','[sigpag]','[vectors]','[vsyscall]','[vdso]','[vvar]','Data']
	os.system(maps)
	os.system(smaps)

	newmapname='newMap'+str(num_PIB)+'.txt'
	#Archivos utilizados y creados
	f=open('maps'+str(num_PIB)+'.txt','r')
	newmap=open(newmapname,'w')
	#Lista para el guardado de la informacion de maps.txt
	lineasArchivo=[]
	#GUardado de las lineas del archivo maps.txt
	mapslineas=f.readlines()
	contmap=0


	#print(smapslineas)

	cont=0
	#Obtencion de informacion de los maps para guardarla en la lista de instancias
	#de tipoInfoArchivo
	tex = 0
	mapeoRex = ""
	mapeoBib = ""
	for i in mapslineas:
		"""
		if(smapslineas[contsmap]==i):
			contsmap+=1
			size=smapslineas[contsmap]
			contsmap+=1
			tamPag=smapslineas[contsmap]
			contsmap+=20
		"""
		#print(size)
		#print(tamPag)
		lineaSeparada=i.split(" ")
		pagina=lineaSeparada[0]
		perm=lineaSeparada[1]
		mapeo=lineaSeparada[len(lineaSeparada)-1]
		mapeo=mapeo.replace("\n","")
		tipo=""
		if mapeo in listaUso:
			if mapeo.find('['):
				tipo=mapeo.replace('[',"")
				tipo=tipo.replace(']',"")
			else:
				tipo = mapeo
		else:
			if(tex > 0 and mapeo == mapeoRex):
				tipo = "Datos"
			elif (tex == 0 and perm.find('r') > -1  and perm.find('x') > -1  and mapeo != ""):
				tipo = "Texto"
				mapeoRex = mapeo
				tex += 1
			elif(tex > 0 and mapeo != mapeoRex and perm.find('r') > -1  and perm.find('x') > -1):
				tipo = "Texto-Bib"
				mapeoBib = mapeo
			elif(tex > 0 and mapeo != mapeoRex and perm.find('r') > -1 and mapeo == mapeoBib) :
				tipo = "Datos-Bib"



		#GUardado de la instancia con la información
		lineasArchivo.append(infoArchivos(tipo,pagina,perm,mapeo))

		cont+=1

	#Impresion en consola, escritura en archivo correspondiente y Escritura a color en el cuadro del Frame2
	print("|| {:20} || {:16} - {:16} || {:15} || {:12} || {:4} || {} \n".format("USO","inicioPagina","FinPagina","Size","Num-pagina","Perm","Uso o mapeo"))
	newmap.write(("|| {:20} || {:16} - {:16} || {:15} || {:12} || {:4} || {} \n".format("USO","inicioPagina","FinPagina","Size","Num-pagina","Perm","Uso o mapeo")))
	action.insert(INSERT,"||")
	action.insert(INSERT," {:7} ".format("USO"),'color_uso')
	action.insert(INSERT,"||")
	action.insert(INSERT," {:16} ".format("Inicio pag"),'color_inicioP')
	action.insert(INSERT,"-")
	action.insert(INSERT," {:16} ".format("FinPagina"),'color_finP')
	action.insert(INSERT,"||")
	action.insert(INSERT," {:15} ".format("Size"),'color_num_size')
	action.insert(INSERT,"||")
	action.insert(INSERT," {:12} ".format("Num-pagina"),'color_num_pag')
	action.insert(INSERT,"||")
	action.insert(INSERT," {:4} ".format("Perm"),'color_permisos')
	action.insert(INSERT,"||")
	action.insert(INSERT," {} \n".format("Uso o Mapeo"),'color_mapeo')
	for i in lineasArchivo:
		print(i.printInfo())
		newmap.write(i.printInfo())
		action.insert(INSERT,"||")
		action.insert(INSERT," {:7} ".format(i.uso),'color_uso')
		action.insert(INSERT,"||")
		action.insert(INSERT," {:16} ".format(i.inicioPagina),'color_inicioP')
		action.insert(INSERT,"-")
		action.insert(INSERT," {:16} ".format(i.finPagina),'color_finP')
		action.insert(INSERT,"||")
		action.insert(INSERT," {:15} ".format(i.num_size),'color_num_size')
		action.insert(INSERT,"||")
		action.insert(INSERT," {:12} ".format(i.num_pag),'color_num_pag')
		action.insert(INSERT,"||")
		action.insert(INSERT," {:4} ".format(i.permisos),'color_permisos')
		action.insert(INSERT,"||")
		action.insert(INSERT," {} \n".format(i.mapeo),'color_mapeo')

	newmap.close()
	f.close()
raiz.mainloop()




 