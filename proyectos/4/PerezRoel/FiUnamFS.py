#Proyecto 4
#de Roel Perez

from sys import argv

def ayuda():
	print("FI UNAM File System")
	print("\t-h\t\tMuestra las funcionalidades del programa.")
	print("\tl\t\tLista el directorio del FiUnamFS.")
	print("\timp <archivo>\tImporta <archivo> de tu sistema hacia el FiUnamFS.")
	print("\texp <archivo\tExp>Exporta <archivo> del FiUnamFS hacia tu sistema.")
	print("\tdel <archivo>\tElimina <archivo> del FiUnamFS.")
	print("\tdf\t\tDesfragmenta FiUnamFS.")
	print("\ts\t\tSalir.")

def list(cmd):
	print('listo');

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
	print("$python3 FiUnamFS.py fiunamfs.img")
	exit(0)
elif len(argv) > 2:
	print("Número inválido de parámetros.")
	exit(0)


fsPath = argv[1]
try:
	fs = open(fsPath, 'r+')
except IOError:
	print('No pudo abrirse el archivo.' + fsPath + '\'')
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
fsTamanioCluster = fs.read(5)
fs.seek(47)
fsTamanioDir = fs.read(2)
fs.seek(52)
fsNumCluster = fs.read(8)


print("FI UNAM File System. Version " + fsVersion )
print("Elaborado por Roel Perez")
print("\t-h\t\tMuestra las funcionalidades del programa.")


inp = ' '

while( inp != 's' ):
	inp = input('>>')
	cmd = inp.split(' ')

	if (cmd[0] == '-h'):
		ayuda()
	elif(cmd[0] == 'l'):
		list(cmd)
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