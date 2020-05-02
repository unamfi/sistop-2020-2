#Proyecto 3
#de Roel Perez

from sys import argv
import traceback

class BloqueMemoria:

	def __init__(self):

		self.dirInicial = ''
		self.dirFinal = ''
		self.permisos = ''
		self.offset = ''
		self.device  = ''
		self.inode = ''
		self.pathname = ''

		self.uso = ''
		self.pagInicial = '' 
		self.pagFinal = ''
		self.numPaginas = 0
		self.tamanioTxt = ''

	def procesarDatos(self):

		self.pagInicial = self.dirInicial[0:len(self.dirInicial)-3]
		self.pagFinal = self.dirFinal[0:len(self.dirFinal)-3]
	
		self.numPaginas = int(self.pagFinal,16) - int(self.pagInicial,16)

		self.tamanioTxt = BloqueMemoria.obtenerTamanio(self.numPaginas)

		if('/' in self.pathname):
			if('x' in self.permisos):
				self.uso = 'texto'
			else:
				self.uso = 'datos'
		elif(self.pathname == '[stack]'):
			self.uso = 'Stack'
		elif(self.pathname == '[heap]'):
			self.uso = 'Heap'
		else:
			self.uso = self.pathname


	def obtenerTamanio(numPaginas):

		tamanio = 4*numPaginas
		unidades = ['KB','MB','GB','TB','PB','EB','ZB','YB','BB']
		contUnidad = 0

		while( (tamanio / 1024) > 1 ):
			contUnidad += 1
			tamanio = tamanio/1024


		tamanioTxt = str(round(tamanio,1)) + ' ' + unidades[contUnidad]

		return tamanioTxt


	def mostrarPagina(self):
		print(self.uso +'\t'+ self.pagInicial +'\t'+ self.pagFinal + '\t' + self.tamanioTxt + '\t' + str(self.numPaginas) + '\t' + self.permisos)


def obtenerBloques(pid, bloques):
	try:
		mapsPath = '/proc/'+pid+'/maps'
		mapsFile = open(mapsPath,'r')

		mapsLineas = mapsFile.readlines()
		for line in mapsLineas:
			bloque = BloqueMemoria()
			
			datosPagina = line.split()
			dirInicioFin = datosPagina[0].split('-')

			bloque.dirInicial = dirInicioFin[0]
			bloque.dirFinal = dirInicioFin[1]
			bloque.permisos = datosPagina[1]
			bloque.offset = datosPagina[2]
			bloque.device = datosPagina[3]
			bloque.inode = datosPagina[4]

			if(len(datosPagina) > 5):
				bloque.pathname = datosPagina[5]
			else:
				bloque.pathname = '[anon]'

			bloque.procesarDatos()

			bloques.append(bloque)

	except Exception as e:
		print(str(e) + traceback.format_exc())
		exit()

	finally: 
		mapsFile.close()

def generarMemoria(bloques, memoria):
	pagLen = len(bloques[0].dirInicial)
	contadorMemoria = '0'*pagLen
	pasadoHeap = False
	for bloque in bloques:
		if(int(bloque.dirInicial,16) > int(contadorMemoria,16)):
			bloqueVacio = BloqueMemoria()
			bloqueVacio.dirInicial = contadorMemoria
			bloqueVacio.dirFinal = bloque.dirInicial
			bloqueVacio.pathname = 'VACIO'
			bloqueVacio.procesarDatos()
			memoria.append(bloqueVacio)

		if(bloque.uso == 'Heap'):
			pasadoHeap = True

		if(pasadoHeap):
			if(bloque.uso == 'texto'):
				bloque.uso = 'Btexto'
			if(bloque.uso == 'datos'):
				bloque.uso = 'Bdatos'

		memoria.append(bloque)
		contadorMemoria = bloque.dirFinal
	
pid = argv[1]

bloques = []
memoria = []

obtenerBloques(pid, bloques)
generarMemoria(bloques,memoria)

for i in memoria:
	i.mostrarPagina()





