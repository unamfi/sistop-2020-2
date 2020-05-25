#Proyecto 4
#de Roel Perez

from sys import argv
import os
import time

class EntradaDir:
	
	def __init__(self):
		self.nombre = ''
		self.tamanio = 0
		self.clusterInicial = 0
		self.creacion = ''
		self.modificacion = ''
		self.reservado = ''


def ayuda():
	print("\th\t\tMuestra las funcionalidades del programa.")
	print("\tl\t\tLista el directorio del FiUnamFS.")
	print("\timp <archivo>\tImporta <archivo> de tu sistema hacia el FiUnamFS.")
	print("\texp <archivo>\tExporta <archivo> del FiUnamFS hacia tu sistema.")
	print("\tdel <archivo>\tElimina <archivo> del FiUnamFS.")
	print("\tdf\t\tDesfragmenta FiUnamFS.")
	print("\ts\t\tSalir.")


def obtenerDirectorio(cmd, fs):

	global fsTamanioCluster, fsTamanioDir

	numEntradas = int((fsTamanioCluster*fsTamanioDir)/64)
	
	fs.seek(1*fsTamanioCluster)

	entradas = []

	for i in range(numEntradas):
		nombre = fs.read(15).decode('ASCII')
		fs.read(1)
		
		if (nombre == 'Xx.xXx.xXx.xXx.'):
			fs.read(48)
			continue

		nombre = stringMenosEspacios(nombre)

		ent = EntradaDir()
		ent.nombre = nombre
		ent.tamanio = int(fs.read(8).decode('ASCII'))
		fs.read(1)
		ent.clusterInicial = int(fs.read(5).decode('ASCII'))
		fs.read(1)
		ent.creacion = fs.read(14).decode('ASCII')
		fs.read(1)
		ent.modificacion = fs.read(14).decode('ASCII')
		fs.read(1)
		ent.reservado = fs.read(3).decode('ASCII')

		entradas.append(ent)

	return entradas


def obtenerTamanio(tamanio):

	unidades = ['B','KB','MB','GB','TB','PB','EB','ZB','YB','BB']
	contUnidad = 0

	while( (tamanio / 1024) >= 1 ):
		contUnidad += 1
		tamanio = tamanio/1024

	tamanioTxt = str(round(tamanio,1)) +' '+ unidades[contUnidad]

	return tamanioTxt


def obtenerFecha(fecha):
	yyyy = fecha[0:4]
	mm = fecha[4:6]
	dd = fecha[6:8]
	hh = fecha[8:10]
	mmin = fecha[10:12]
	ss = fecha[12:14]

	fechaTxt = dd + '/' + mm + '/' + yyyy + ' ' + hh + ':' + mmin + ':' + ss

	return fechaTxt


def listarDirectorio(directorio):
	if(len(cmd) > 1):
		print('Número inválido de argumentos.')
		return -1

	print('Nombre'+(' '*9)+'\t\tTamaño\t\tCreacion\t\tUltima modificacion')
	for ent in directorio:
		
		print(ent.nombre + '\t\t' , end= '')

		tamanio = obtenerTamanio(ent.tamanio)
		print(tamanio+ ' '*(12-len(tamanio)) +'\t',end='')

		print(obtenerFecha(ent.creacion) + '\t',end='')

		print(obtenerFecha(ent.modificacion))

		#########################
		print(ent.clusterInicial)
		#########################

def generarBitmap(bm, dir):

	for ent in dir:
		numClusters = tamanioEnClusters(int(ent.tamanio))
		for i in range(ent.clusterInicial,ent.clusterInicial+numClusters):
			bm[i] = True


def tamanioEnClusters(tamanioEnBytes):

	global fsTamanioCluster

	#Equivalente a funcion ceil()
	return (tamanioEnBytes+(fsTamanioCluster-1))//fsTamanioCluster


def importar(cmd, fs):
	if(len(cmd) != 2):
		print('Número inválido de argumentos.')
		return -1

	global fsTamanioCluster

	try:
		f = open(cmd[1], 'rb')
		entradaDir = generarEntrada(cmd[1])
	except IOError:
		print('No pudo abrirse el archivo \'' + cmd[1] + '\'')
		return -1
	except FileNotFoundError:
		print('El archivo \'' + cmd[1] + '\' no se encuentra.')
		return -1

	entradaIndice = buscarEntradaDirLibre(fs)
	if (entradaIndice == -1):
		print("No hay entradas disponibles en el directorio.")

	clusterInicialIndice = buscarBloquesContiguos(tamanioEnClusters(entradaDir.tamanio))
	if (clusterInicialIndice == -1):
		print('No hay bloques contiguos en la unidad para almacenar \'' + cmd[1] + '\'')

	entradaDir.clusterInicial = clusterInicialIndice

	escribirEntrada(fs, entradaDir, entradaIndice)
	
	fs.seek(fsTamanioCluster*entradaDir.clusterInicial)
	fs.write(f.read())
	f.close()

	print('Se ha importado \'' + cmd[1] + '\' al FiUnamFS.')


def generarEntrada(pathname):
	entradaDir = EntradaDir()
	
	entradaDir.nombre = os.path.basename(pathname)
	entradaDir.tamanio = os.path.getsize(pathname)
	entradaDir.creacion = fechaEnFormato(os.path.getctime(pathname))
	entradaDir.modificacion = fechaEnFormato(os.path.getmtime(pathname))
	
	return entradaDir


def fechaEnFormato(segsDesdeEpoch):
	datetime = time.gmtime(segsDesdeEpoch)
	yyyy = str(datetime.tm_year).rjust(4,'0')
	mm = str(datetime.tm_mon).rjust(2,'0')
	dd = str(datetime.tm_mday).rjust(2,'0')
	hh = str(datetime.tm_hour).rjust(2,'0')
	mmin = str(datetime.tm_min).rjust(2,'0')
	ss = str(datetime.tm_sec).rjust(2,'0')

	return yyyy + mm + dd + hh + mmin + ss


def buscarBloquesContiguos(numClusters):

	global bitmap 

	cuentaCluster = 0
	for i in range(len(bitmap)):
		if(bitmap[i] == False):
			cuentaCluster += 1
			if cuentaCluster == numClusters:
				clusterInicial = i - numClusters + 1
				for j in range(clusterInicial, clusterInicial+numClusters):
					bitmap[j] = True
				return clusterInicial
		else:
			cuentaCluster = 0

	return -1 


def buscarEntradaDirLibre(fs):
	global fsTamanioCluster, fsTamanio

	numEntradas = int((fsTamanioCluster*fsTamanioDir)/64)
	
	fs.seek(1*fsTamanioCluster)

	for i in range(numEntradas):
		nombre = fs.read(15).decode('ASCII')
		
		if (nombre == 'Xx.xXx.xXx.xXx.'):
			return i

		fs.read(64-15)

	return -1


def escribirEntrada(fs, ent, entIndice):
	global fsTamanioCluster
	fs.seek(1*fsTamanioCluster + 64*entIndice)

	fs.write( ent.nombre.rjust(15,' ').encode('ASCII') )
	fs.write(b'\x00')
	fs.write( str(ent.tamanio).rjust(8,'0').encode('ASCII') )
	fs.write(b'\x00')
	fs.write( str(ent.clusterInicial).rjust(5,'0').encode('ASCII') )
	fs.write(b'\x00')
	fs.write( ent.creacion.encode('ASCII') )
	fs.write(b'\x00')
	fs.write( ent.modificacion.encode('ASCII') )
	fs.write(b'\x00')


def exportar(cmd, fs, directorio):
	
	global fsTamanioCluster

	if(len(cmd) != 2):
		print('Número inválido de argumentos.')
		return -1

	archivoInd = buscarArchivo(cmd[1],directorio)

	if archivoInd == -1:
		print('El archivo \'' + cmd[1] + '\' no se encuentra en el FIUnamFS.')
		return -1

	archivo = directorio[archivoInd]

	try:
		expF = open(archivo.nombre,'w+b')
	except IOError:
		print('No se pudo exportar el archivo.')
		return -1

	fs.seek(fsTamanioCluster*archivo.clusterInicial)
	expF.write(fs.read(archivo.tamanio))
	expF.close()

	print('Se ha transferido \'' + cmd[1] + '\' a tu sistema.')



def buscarArchivo(archivo,directorio):
	index = 0
	for ent in directorio:
		if archivo == ent.nombre:
			return index
		index += 1
	return -1


def stringMenosEspacios(str):
	strLista = str.split()

	retString = ''
	for i in strLista:
		retString = retString + i 

	return retString


def eliminar(cmd, fs, directorio):
	if(len(cmd) != 2):
		print('Número inválido de argumentos.')
		return -1

	global fsTamanioCluster, bitmap

	archivoIndex = buscarArchivo(cmd[1],directorio)

	clusterInicial = directorio[archivoIndex].clusterInicial
	numClusters = tamanioEnClusters(directorio[archivoIndex].tamanio)
	for i in range(clusterInicial, clusterInicial+numClusters):
		bitmap[i] = False

	fs.seek(1*fsTamanioCluster + 64*archivoIndex)
	fs.write(b'Xx.xXx.xXx.xXx.')


def desfragmentar(cmd):
	print('desfragmento')




#Inicio del programa

if (len(argv) < 2):
	print("Ingresa como argumento el nombre o la ruta al sistema de archivos. Ejemplo:")
	print("$ python3 FiUnamFS.py fiunamfs.img")
	exit(0)
elif len(argv) > 2:
	print("Número inválido de parámetros.")
	exit(0)


fsPath = argv[1]
try:
	fs = open(fsPath, 'r+b')
except IOError:
	print('No pudo abrirse el archivo \'' + fsPath + '\'')
	exit(0)


fs.seek(0) 
fsAut = fs.read(8)

if (fsAut != 'FiUnamFS'.encode('ASCII')):
	print('\''+ fsPath +'\' no es un sistema de archivos FiUnamFS.')
	fs.close()
	exit()

fs.seek(10)
fsVersion = fs.read(3).decode('ASCII')
fs.seek(20)
fsVolumen = fs.read(15).decode('ASCII')
fs.seek(40)
fsTamanioCluster = int(fs.read(5).decode('ASCII'))
fs.seek(47)
fsTamanioDir = int(fs.read(2).decode('ASCII'))
fs.seek(52)
fsNumCluster = int(fs.read(8).decode('ASCII'))


#Bitmap de la memoria disponible/ocupada
bitmap = 5*[True] + (fsNumCluster-5)*[False]
generarBitmap(bitmap, obtenerDirectorio('',fs))


print("FI UNAM File System. Version " + fsVersion)
print("Elaborado por Roel Perez")
print("Escribe \"h\" para mostrar las funcionalidades del programa.")


inp = ' '

while( inp != 's' ):
	inp = input('>> ')
	cmd = inp.split()

	if len(cmd) == 0:
		continue

	if (cmd[0] == 'h'):
		ayuda()
	elif(cmd[0] == 'l'):
		directorio = obtenerDirectorio(cmd,fs)
		listarDirectorio(directorio)
	elif(cmd[0] == 'imp'):
		importar(cmd,fs)
	elif(cmd[0] == 'exp'):
		directorio = obtenerDirectorio(cmd,fs)
		exportar(cmd,fs,directorio)
	elif(cmd[0] == 'del'):
		directorio = obtenerDirectorio(cmd,fs)
		eliminar(cmd,fs,directorio)
	elif(cmd[0] == 'df'):
		desfragmentar(cmd)
	elif(cmd[0] == 's'):
		fs.close()
	else:
		print('Comando no reconocido.')