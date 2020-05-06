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
				self.uso = 'Texto'
			elif(not ('r' in self.permisos) and not('w' in self.permisos) and not('x' in self.permisos)):
				self.uso = 'Reserva'
			else:
				self.uso = 'Datos'
		elif(self.pathname == '[stack]'):
			self.uso = 'Stack'
		elif(self.pathname == '[heap]'):
			self.uso = 'Heap'
		elif(self.pathname == 'Vacio'):
			self.uso = '...'
		else:
			self.uso = self.pathname


	def obtenerTamanio(numPaginas):

		tamanio = 4*numPaginas
		unidades = ['KB','MB','GB','TB','PB','EB','ZB','YB','BB']
		contUnidad = 0

		while( (tamanio / 1024) >= 1 ):
			contUnidad += 1
			tamanio = tamanio/1024


		tamanioTxt = str(round(tamanio,1)) + unidades[contUnidad]

		return tamanioTxt

	"""
	def mostrarPagina(self):
		print(self.uso +'\t'+ self.pagInicial +'-'+ self.pagFinal + '\t' + self.tamanioTxt + '\t' + str(self.numPaginas) + '\t' + self.permisos + '\t' + self.pathname)
	"""

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
			bloque.permisos = datosPagina[1][0:3]
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
			bloqueVacio.pathname = 'Vacio'
			bloqueVacio.procesarDatos()
			memoria.append(bloqueVacio)

		if(bloque.uso == 'Heap'):
			pasadoHeap = True

		if(pasadoHeap):
			if(bloque.uso == 'Texto'):
				bloque.uso = 'Bib Texto'
			if(bloque.uso == 'Datos'):
				bloque.uso = 'Bib Datos'

		memoria.append(bloque)
		contadorMemoria = bloque.dirFinal

def mostrarMemoria(memoria):

	colorUso = {
		"Heap":"\033[32mHeap\033[m",
		"Stack":"\033[31mStack\033[m",
		"Datos":"\033[34mDatos\033[m",
		"Texto":"\033[35mTexto\033[m",
		"Bib Datos":"\033[36mBib \033[34mDatos\033[m",
		"Bib Texto":"\033[36mBib \033[35mTexto\033[m",
		"Vacio":"Vacio",
		"[anon]":"\033[33m[anon]\033[m",
		"[vvar]":"\033[33m[vvar]\033[m",
		"[vdso]":"\033[33m[vdso]\033[m",
		"[vsyscall]":"\033[33m[vsyscall]\033[m"
	}


	#longitud de cada columna
	dirLen = len(memoria[len(memoria)-1].pagInicial)
	usoLen = 15
	tamanoLen = 12
	numPaginasLen = 10
	permisosLen = 5

	print("\033[4m",end="")
	print("|"+ centrarCadena('[Ini-Fin)',(dirLen*2)+1),end='')
	print("|"+centrarCadena('Uso',usoLen),end='')
	print("|"+centrarCadena('Tamaño',tamanoLen),end='')
	print("|"+centrarCadena('Num. págs.',numPaginasLen),end='')
	print("|"+centrarCadena('Perm.',permisosLen),end='')
	print("|"+' Uso/Mapeo')
	print("\033[m",end="")

	for i in reversed(memoria):

		desdePag = '0'*(dirLen-len(i.pagInicial)) + i.pagInicial
		hastaPag = '0'*(dirLen-len(i.pagFinal)) + i.pagFinal

		print(' '+desdePag+'-'+hastaPag,end='')

		espacioUso = usoLen - len(i.uso)
		if(espacioUso % 2 == 0):
			print('|'+(espacioUso//2)*' ' + colorUso.get(i.uso,i.uso) +(espacioUso//2)*' '+'|',end='')
		else: 
			print('|'+(espacioUso//2)*' ' + colorUso.get(i.uso,i.uso) +((espacioUso//2)+1)*' '+'|',end='')

		print(centrarCadena(i.tamanioTxt,tamanoLen)+' ',end='')

		if(i.numPaginas > 99999999):
			tamanioRedondeado = i.numPaginas
			contDiv = 0
			while((tamanioRedondeado/1000)>1):
				tamanioRedondeado /= 1000
				contDiv += 1
			tamanioReducido = str(round(tamanioRedondeado,2))+'E'+str(contDiv*3)
		else:
			tamanioReducido = str(i.numPaginas)

		print(centrarCadena(tamanioReducido,numPaginasLen) + ' ',end='')

		print(centrarCadena(i.permisos,permisosLen) + ' ',end='')

		if('/' in i.pathname):
			print("..."+i.pathname[i.pathname.rfind('/'):])
		else:
			print(i.pathname)


		


	"""
	print(colorUso["Heap"])
	print(colorUso["Stack"])
	print(colorUso["Datos"])
	print(colorUso["Texto"])
	print(colorUso["Bib. Datos"])
	print(colorUso["Bib. Texto"])
	print(colorUso["[anon]"])
	"""

def centrarCadena(cadena,tamano):
	if len(cadena) >= tamano:
		return cadena
	else:
		espacio = tamano - len(cadena)
		if (espacio%2 == 0):
			return (espacio//2)*" " + cadena + (espacio//2)*" "  
		else: 
			return ((espacio)//2)*" " + cadena + (((espacio)//2)+1)*" "  


	
pid = argv[1]

bloques = []
memoria = []

obtenerBloques(pid, bloques)
generarMemoria(bloques,memoria)

mostrarMemoria(memoria)

"""
for i in memoria:
	i.mostrarPagina()
"""




