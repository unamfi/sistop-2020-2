import os
import time

#NOTA: en las instrucciones donde se obtienen los datos del sistema de archivos se le quita un caracter [:-1] esto es para que fuera consistente con los archivos
#      que usted puso por que contienen un caracter nulo al final, por lo que el maximo del nombre de archivo lo reduje a 15

def encontrar_archivo(archivo_a_encontrar, sistema_de_archivos, tamano_de_cluster):

	#se posisciona en el cluster del directorio
	sistema_de_archivos.seek(tamano_de_cluster)

	#recorre las entradas del directorio
	for i in range(0, tamano_de_cluster * 4, 64):
		sistema_de_archivos.seek(tamano_de_cluster+i)
		#se le asigna los datos leidos correspondiente al nombre quitando un caracter nulo al final
		archivo = sistema_de_archivos.read(16).decode("utf-8").strip()[:-1]
		if archivo == archivo_a_encontrar:

			tamano_archivo = int(sistema_de_archivos.read(9).decode("utf-8")[:-1])
			cluster_inicial = int(sistema_de_archivos.read(6).decode("utf-8")[:-1])

			return (tamano_archivo, cluster_inicial)
		
	return (0,0)

	

def listar_contenido(sistema_de_archivos, tamano_de_cluster):
	print("\n\n   << LISTA DE CONTENIDO >>\n")
	sistema_de_archivos.seek(tamano_de_cluster)

	for i in range(0, tamano_de_cluster * 4, 64):
		sistema_de_archivos.seek(tamano_de_cluster+i)
		archivo = sistema_de_archivos.read(16).decode("utf-8")
		if archivo[:15] != "Xx.xXx.xXx.xXx.":
			print("\n---> Archivo:", archivo.strip()[:-1])
			print("          Tamano:",int(sistema_de_archivos.read(9).decode("utf-8")[:-1])," Cluster inicial:",int(sistema_de_archivos.read(6).decode("utf-8")[:-1]))


def copiar_hacia_sistema(sistema_de_archivos, tamano_de_cluster):
	print("\n\n   << COPIAR HACIA SISTEMA >>\n")

	archivo_a_copiar = input("Ingrese nombre del archivo a copiar al sistema: ")

	datos_archivo = encontrar_archivo(archivo_a_copiar, sistema_de_archivos, tamano_de_cluster)

	#se asignan los datos correspondientes de la tupla
	tamano_archivo = datos_archivo[0]
	cluster_inicial = datos_archivo[1]

	#si no tiene tamano ni cluster inicial entonces no se encontro el archivo
	if tamano_archivo == 0 and cluster_inicial == 0:
		print("\nEl archivo no se encontro en FiUnamFs")

	else:

		print("\n---> Archivo encontrado:", archivo_a_copiar)
		print("          Tamano:", tamano_archivo," Cluster inicial:", cluster_inicial)

		nuevo_archivo = open("(Desde FiUnamFs)"+archivo_a_copiar,"wb")

		sistema_de_archivos.seek(tamano_de_cluster * cluster_inicial)
		nuevo_archivo.write(sistema_de_archivos.read(tamano_archivo))

		nuevo_archivo.close()

		print("\n¡Archivo copiado a sistema con exito!")

def obtener_dir_de_siguiente_cluster(cluster_inicial, tamano_archivo, tamano_de_cluster):
	sobrante = tamano_archivo%tamano_de_cluster
	valor_a_aumentar = 1024 - sobrante

	return (cluster_inicial) * 1024 + tamano_archivo + valor_a_aumentar


def obtener_espacio_de_directorio(sistema_de_archivos, tamano_de_cluster):
	sistema_de_archivos.seek(tamano_de_cluster)

	for i in range(0, tamano_de_cluster * 4, 64):
		sistema_de_archivos.seek(tamano_de_cluster+i)
		archivo = sistema_de_archivos.read(16).decode("utf-8")
		if archivo[:15] == "Xx.xXx.xXx.xXx.":
			return tamano_de_cluster + i

	return -1


def obtener_cluster_disponible(tamano_de_archivo_a_copiar, sistema_de_archivos, tamano_de_cluster, tamano_sistema_de_archivos):
	sistema_de_archivos.seek(tamano_de_cluster)
	datos_archivos = []
	for i in range(0, tamano_de_cluster * 4, 64):
		sistema_de_archivos.seek(tamano_de_cluster+i)

		archivo = sistema_de_archivos.read(16).decode("utf-8").strip()[:-1]

		if archivo[:15] != "Xx.xXx.xXx.xXx.":
			tamano_archivo = int(sistema_de_archivos.read(9).decode("utf-8")[:-1])
			cluster_inicial = int(sistema_de_archivos.read(6).decode("utf-8")[:-1])

			#se agrega a una lista donde se contienen los datos esenciales de los archivos
			datos_archivos.append((cluster_inicial,tamano_archivo))

	
	#se ordenan los datos esenciales de los archivos con respecto a su cluster inicial
	datos_archivos = sorted(datos_archivos, key=lambda x: x[0])

	for i in range(0,len(datos_archivos)):

		dir_cluster_Siguiente = obtener_dir_de_siguiente_cluster(datos_archivos[i][0], datos_archivos[i][1], tamano_de_cluster)

		#si son los ultimos datos de los archivos la comparacion es con el tamaño del archivo 
		if i == len(datos_archivos)-1:
			espacio_libre = tamano_sistema_de_archivos - dir_cluster_Siguiente
		#si no entonces la comparacion es con el archivo siguiente
		else:
			dir_cluster_archivo_siguiente = datos_archivos[i+1][0] * 1024
			espacio_libre = dir_cluster_archivo_siguiente - dir_cluster_Siguiente

		if espacio_libre >= tamano_de_archivo_a_copiar:
			return dir_cluster_Siguiente
	return -1
			



def copiar_hacia_fiunamfs(sistema_de_archivos, tamano_sistema_de_archivos, tamano_de_cluster):
	print("\n\n   << COPIAR HACIA FIUNAMFS >>\n")
	archivo_a_copiar = input("\nIngrese nombre del archivo a copiar a FiUnamFs: ")

	if len(archivo_a_copiar) > 15:
		print("\nEl nombre del archivo no puede tener una longitud mayor a 15.")
		return

	if os.path.isfile(archivo_a_copiar) == False:
		print("\nEl archivo no existe o es invalido.")
		return
	#se obtienen los datos esenciales del archivo y se ponen en una tupla
	datos_archivo = encontrar_archivo(archivo_a_copiar, sistema_de_archivos, tamano_de_cluster)

	#se obtienen los datos de la tupla
	tamano_archivo = datos_archivo[0]
	cluster_inicial = datos_archivo[1]

	if tamano_archivo == 0 and cluster_inicial == 0:
		
		tamano_archivo_a_copiar = os.stat(archivo_a_copiar).st_size

		print("\nTamano de archivo:", tamano_archivo_a_copiar)

		direccion = obtener_espacio_de_directorio(sistema_de_archivos, tamano_de_cluster)

		if direccion == -1:
			print("\nEl directorio ya está lleno ¡lo siento!")
			return

		dir_cluster_disponible = obtener_cluster_disponible(tamano_archivo_a_copiar, sistema_de_archivos, tamano_de_cluster, tamano_sistema_de_archivos)

		if dir_cluster_disponible == -1:
			print("\nEl archivo no cabe en el sistema_de_archivos ¡lo siento!")
			return

		sistema_de_archivos.seek(direccion)
		sistema_de_archivos.write("                ".encode("utf-8"))
		sistema_de_archivos.seek(direccion)
		archivo_a_copiar = archivo_a_copiar + "."
		sistema_de_archivos.write(archivo_a_copiar.encode("utf-8"))


		sistema_de_archivos.seek(direccion+16)
		sistema_de_archivos.write("000000000".encode("utf-8"))
		str_tamano_archivo_a_copiar = str(tamano_archivo_a_copiar)
		str_tamano_archivo_a_copiar = str_tamano_archivo_a_copiar + "."
		numero_ceros = 9 - len(str_tamano_archivo_a_copiar)
		sistema_de_archivos.seek(direccion + 16 + numero_ceros)
		sistema_de_archivos.write(str_tamano_archivo_a_copiar.encode("utf-8"))


		sistema_de_archivos.seek(direccion+25)
		sistema_de_archivos.write("000000".encode("utf-8"))
		cluster_disponible = int(dir_cluster_disponible / 1024)
		str_cluster_disponible= str(cluster_disponible)
		str_cluster_disponible = str_cluster_disponible + "."
		numero_ceros = 6 - len(str_cluster_disponible)
		sistema_de_archivos.seek(direccion + 25 + numero_ceros)
		sistema_de_archivos.write(str_cluster_disponible.encode("utf-8"))

		
		sistema_de_archivos.seek(direccion+31)
		str_fecha = str(time.localtime().tm_year) + str(time.localtime().tm_mon).zfill(2) + str(time.localtime().tm_mday).zfill(2) + str(time.localtime().tm_hour).zfill(2) + str(time.localtime().tm_min).zfill(2) + str(time.localtime().tm_sec).zfill(2)
		str_fecha = str_fecha + "."
		sistema_de_archivos.write(str_fecha.encode("utf-8"))


		sistema_de_archivos.seek(direccion+46)
		sistema_de_archivos.write(str_fecha.encode("utf-8"))


		contenido_archivo = open(archivo_a_copiar[:-1], "r+b")
		sistema_de_archivos.seek(dir_cluster_disponible)
		for elemento in contenido_archivo:
			sistema_de_archivos.write(elemento)

		print("\n¡Archivo copiado a FiUnamFs con exito!")

		


	else:

		print("\nEl archivo ya existe en FiUnamFs, considera renombrarlo")

def eliminar_de_fiunamfs(sistema_de_archivos, tamano_de_cluster):
	print("\n\n   << ELIMINAR DE SISTEMA >>\n")

	archivo_a_eliminar = input("Ingrese nombre del archivo a eliminar del sistema: ")

	sistema_de_archivos.seek(tamano_de_cluster)

	#recorre las entradas del directorio
	for i in range(0, tamano_de_cluster * 4, 64):
		sistema_de_archivos.seek(tamano_de_cluster+i)
		#se le asigna los datos leidos correspondiente al nombre quitando un caracter nulo al final
		archivo = sistema_de_archivos.read(16).decode("utf-8").strip()[:-1]
		if archivo == archivo_a_eliminar:
			sistema_de_archivos.seek(tamano_de_cluster+i)
			sistema_de_archivos.write("Xx.xXx.xXx.xXx.".encode("utf-8"))

			print("\n¡Archivo eliminado de FiUnamFs con exito!")
			return

	print("\nEl archivo no se encontro en FiUnamFs")


			


def main():

	tamano_de_sector = 256
	tamano_de_cluster = tamano_de_sector * 4

	sistema_de_archivos = open("fiunamfs.img", "r+b")

	print("\n\n   <---- SISTEMA DE ARCHIVOS FiUnamFs ---->\n\n")

	sistema_de_archivos.seek(0)
	print("Nombre de sistema de archivos:", sistema_de_archivos.read(9).decode("utf-8"))
	print("Versión de la implementación:", sistema_de_archivos.read(4).decode("utf-8"))
	sistema_de_archivos.seek(20)
	print("Etiqueta del volumen:", sistema_de_archivos.read(16).decode("utf-8"))
	sistema_de_archivos.seek(40)
	print("Tamaño del cluster en bytes:", sistema_de_archivos.read(6).decode("utf-8"))
	sistema_de_archivos.seek(47)
	print("Número de clusters que mide el directorio:", sistema_de_archivos.read(3).decode("utf-8"))
	sistema_de_archivos.seek(52)
	print("Número de clusters que mide la unidad completa:", sistema_de_archivos.read(9).decode("utf-8"))

	opcion = ""

	#ciclo del menu
	while(opcion != "5"):

		#se debe reabrir cada vez el archivo para mostrar los cambios
		sistema_de_archivos = open("fiunamfs.img", "r+b")

		tamano_sistema_de_archivos = os.stat("fiunamfs.img").st_size

		print("\n-----------------------------------------------------------------------\n\n   << MENU >>\n")
		print("1. Listar contenido")
		print("2. Copiar archivo de FiUnamFS hacia tu sistema")
		print("3. Copiar archivo de tu sistema hacia FiUnamFS")
		print("4. Eliminar archivo de FiUnamFS")
		print("5. Salir")

		opcion = input("\n\nIngresa una opción: ")

		if opcion == "1":
			listar_contenido(sistema_de_archivos, tamano_de_cluster)

		elif opcion == "2":
			copiar_hacia_sistema(sistema_de_archivos, tamano_de_cluster)

		elif opcion == "3":
			copiar_hacia_fiunamfs(sistema_de_archivos, tamano_sistema_de_archivos, tamano_de_cluster)

		elif opcion == "4":
			eliminar_de_fiunamfs(sistema_de_archivos, tamano_de_cluster)

		#se debe cerrar el archivo en cada ciclo para mostrar los cambios 
		sistema_de_archivos.close()

main()