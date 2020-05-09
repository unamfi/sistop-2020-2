#biblioteca para mostrar el texto en columnas correctamente
from columnar import columnar

#para las columnas, los encabezados
encabezados = [' USO ', ' PAGINA INICIAL ', ' PAGINA FINAL ', ' BYTES ', ' PAGINAS ', ' PERMISO ', ' MAPEO O USO ']

print("\n\n   <---- MAPA DE MEMORIA DE PROCESOS ---->")

proceso = input("\n\n  Ingresa PID de proceso a analizar: ")

#archivos es la primera lista generada con la informacon sustancial
archivos = []

direccion = "/proc/"+proceso+"/maps"

maps = open(direccion, "r")

for linea in maps:
	linea_separada = linea.split()

	paginas = linea_separada[0].split("-") #se obtienen las paginas separando por el guion

	permisos = linea_separada[1]

	if(len(linea_separada) == 6):
		ubicacion = linea_separada[5]  #si no hay mapeo entonces es vacio
	else:
		ubicacion = "---- Vacio ----"

	#se agregan los elementos obtenidos, quitando los ultimos 3 caracteres que corresponden a los 4096 bytes de cada pagina
	archivos.append([paginas[0][:-3], paginas[1][:-3], permisos, ubicacion]) 

#lista es la segunda lista generada a partir de lla informacion sustancial y donde se identifican las secciones de memoria
lista = []

print("\n\n\n LISTA: \n\n")


for elemento in archivos:

	uso = ""

	if(elemento[3][0] == "/"):

		#para identificar si es libreria
		if(elemento[3][0:4] == "/lib" or elemento[3][0:8] == "/usr/lib"):
			uso = "Bib->"

		#para identificar si es ejecutable, entonces es texto
		if(elemento[2][2] == "x"):
			uso = uso + "Texto"
		else:
			uso = uso + "Datos"

	else:
		#si no es texto ni datos
		uso = elemento[3]

	#se calcula el numero de paginas haciendo una resta
	paginas = int(elemento[1],16)-int(elemento[0],16)

	lista.append([uso, elemento[0], elemento[1], paginas * 4000, paginas, elemento[2], elemento[3]])

#se imprime la tabla
tabla= columnar(lista, encabezados, no_borders=False)
print(tabla)


