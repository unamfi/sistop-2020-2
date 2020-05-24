#Proyecto 4
#de Roel Perez

from sys import argv

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
	print("\texp <archivo\tExp>Exporta <archivo> del FiUnamFS hacia tu sistema.")
	print("\tdel <archivo>\tElimina <archivo> del FiUnamFS.")
	print("\tdf\t\tDesfragmenta FiUnamFS.")
	print("\ts\t\tSalir.")


def obtenerDirectorio(cmd, fs, tamanioCluster, tamanioDir):
	if(len(cmd) > 1):
		print('Número inválido de argumentos.')
		return -1

	numEntradas = int((tamanioCluster*tamanioDir)/64)
	
	fs.seek(1*tamanioCluster)

	entradas = []

	for i in range(numEntradas):
		nombre = fs.read(15)
		fs.read(1)
		
		if (nombre == 'Xx.xXx.xXx.xXx.'):
			fs.read(48)
			continue
		ent = EntradaDir()
		ent.nombre = nombre
		ent.tamanio = fs.read(8)
		fs.read(1)
		ent.clusterInicial = fs.read(5)
		fs.read(1)
		ent.creacion = fs.read(14)
		fs.read(1)
		ent.modificacion = fs.read(14)
		fs.read(1)
		ent.reservado = fs.read(3)

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
	print('Nombre'+(' '*9)+'\t\tTamaño\t\tCreacion\t\tUltima modificacion')
	for ent in directorio:
		
		print(ent.nombre + '\t\t' , end= '')

		tamanio = obtenerTamanio(int(ent.tamanio))
		print(tamanio+ ' '*(12-len(tamanio)) +'\t',end='')

		print(obtenerFecha(ent.creacion) + '\t',end='')

		print(obtenerFecha(ent.modificacion))


def importar(cmd):
	print('importo')

def exportar(cmd):
	print('exporto')

def eliminar(cmd):
	print('elimino')

def desfragmentar(cmd):
	print('desfragmento')


if (len(argv) < 2):
	print("Ingresa como argumento el nombre o la ruta al sistema de archivos. Ejemplo:")
	print("$ python3 FiUnamFS.py fiunamfs.img")
	exit(0)
elif len(argv) > 2:
	print("Número inválido de parámetros.")
	exit(0)


fsPath = argv[1]
try:
	fs = open(fsPath, 'r+')
except IOError:
	print('No pudo abrirse el archivo \'' + fsPath + '\'')
	exit(0)


fs.seek(0) 
fsAut = fs.read(8)

if (fsAut != 'FiUnamFS'):
	print('\''+ fsPath +'\' no es un sistema de archivos FiUnamFS.')
	fs.close()
	exit()

fs.seek(10)
fsVersion = fs.read(3)
fs.seek(20)
fsVolumen = fs.read(15)
fs.seek(40)
fsTamanioCluster = int(fs.read(5))
fs.seek(47)
fsTamanioDir = int(fs.read(2))
fs.seek(52)
fsNumCluster = int(fs.read(8))


print("FI UNAM File System. Version " + fsVersion )
print("Elaborado por Roel Perez")
print("Escribe \"h\" para mostrar las funcionalidades del programa.")


inp = ' '

while( inp != 's' ):
	inp = input('>> ')
	cmd = inp.split(' ')

	if (cmd[0] == 'h'):
		ayuda()
	elif(cmd[0] == 'l'):
		directorio = obtenerDirectorio(cmd, fs, fsTamanioCluster, fsTamanioDir)
		listarDirectorio(directorio)
	elif(cmd[0] == 'imp'):
		importar(cmd)
	elif(cmd[0] == 'exp'):
		exportar(cmd)
	elif(cmd[0] == 'del'):
		eliminar(cmd)
	elif(cmd[0] == 'df'):
		desfragmentar(cmd)
	elif(cmd[0] == 's'):
		fs.close()
	else:
		print('Comando no reconocido.')