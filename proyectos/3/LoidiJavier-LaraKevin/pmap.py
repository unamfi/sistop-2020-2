from columnar import columnar

headers = [' USO ', ' PAGINA INICIAL ', ' PAGINA FINAL ', ' BYTES ', ' PAGINAS ', ' PERMISO ', ' MAPEO O USO ']

print("\n\n   <---- MAPA DE MEMORIA DE PROCESOS ---->")


proceso = input("\n\n  Ingresa PID de proceso a analizar: ")

archivos = []

direccion = "/proc/"+proceso+"/maps"

maps = open(direccion, "r")

for linea in maps:
	linea_separada = linea.split()

	paginas = linea_separada[0].split("-")

	permisos = linea_separada[1]

	if(len(linea_separada) == 6):
		ubicacion = linea_separada[5]
	else:
		ubicacion = "---- Vacio ----"


	archivos.append([paginas[0][:-3], paginas[1][:-3], permisos, ubicacion])

lista = []

print("\n\n\n LISTA: \n\n")


for elemento in archivos:

	uso = ""

	if(elemento[3][0] == "/"):
	
		if(elemento[3][0:4] == "/lib" or elemento[3][0:8] == "/usr/lib"):
			uso = "Bib->"

		if(elemento[2][2] == "x"):
			uso = uso + "Texto"
		else:
			uso = uso + "Datos"

	else:
		uso = elemento[3]

	paginas = int(elemento[1],16)-int(elemento[0],16)

	lista.append([uso, elemento[0], elemento[1], paginas * 4000, paginas, elemento[2], elemento[3]])


table = columnar(lista, headers, no_borders=False)
print(table)

