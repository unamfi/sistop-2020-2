tamano_de_sector = 256
tamano_de_cluster = tamano_de_sector * 4

sistema_de_archivos = open("fiunamfs.img", "rb+")


def listar_contenido():
	print("\n\n   << LISTA DE CONTENIDO >>\n")
	sistema_de_archivos.seek(tamano_de_cluster)

	for i in range(0, tamano_de_cluster * 4, 64):
		sistema_de_archivos.seek(tamano_de_cluster+i)
		archivo = sistema_de_archivos.read(16).decode("utf-8")
		if archivo[:15] != "Xx.xXx.xXx.xXx.":
			print("Archivo:", archivo.strip()[:-1])

	#print("\n FUERA:", sistema_de_archivos.read(64).decode("utf-8"))

def copiar_hacia_sistema():
	print("\n\n   << COPIAR HACIA SISTEMA >>\n")
	sistema_de_archivos.seek(tamano_de_cluster)

	archivo_a_copiar = input("Ingrese nombre del archivo a copiar al sistema: ")

	encontrado = False

	for i in range(0, tamano_de_cluster * 4, 64):
		sistema_de_archivos.seek(tamano_de_cluster+i)
		archivo = sistema_de_archivos.read(16).decode("utf-8").strip()[:-1]
		if archivo == archivo_a_copiar:
			print("Archivo encontrado:", archivo)
			encontrado = True
			break

	if encontrado == True:

		nuevo_archivo = open(archivo,"wb")

		tamano_archivo = int(sistema_de_archivos.read(9).decode("utf-8")[:-1])
		print("Tamaño de archivo en bytes:", tamano_archivo)
		cluster_inicial = int(sistema_de_archivos.read(5).decode("utf-8"))
		print("Cluster inicial:", cluster_inicial)

		sistema_de_archivos.seek(tamano_de_cluster * cluster_inicial)
		nuevo_archivo.write(sistema_de_archivos.read(tamano_archivo))

		nuevo_archivo.close()


	else:
		print("El archivo no se encontro en FiUnamFs")


def copiar_hacia_fiunamfs():
	print("COPIANDO HACIA FIUNAMFS")


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

while(opcion != "6"):
	print("\n-----------------------------------------------------------------------\n\n   << MENU >>\n")
	print("1. Listar contenido")
	print("2. Copiar archivo de FiUnamFS hacia tu sistema")
	print("3. Copiar archivo de tu sistema hacia FiUnamFS")
	print("4. Eliminar archivo de FiUnamFS")
	print("5. Desfragmentar FiUnamFS")
	print("6. Salir")

	opcion = input("\n\nIngresa una opción: ")

	if opcion == "1":
		listar_contenido()
	elif opcion == "2":
		copiar_hacia_sistema()
	elif opcion == "3":
		copiar_hacia_fiunamfs()





#for linea in sistema_de_archivos:
#	print(linea)
#	print("FIN LINEA")
	#linea_separada = linea.split()