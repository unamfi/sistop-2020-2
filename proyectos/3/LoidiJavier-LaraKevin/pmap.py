proceso = input("\n\n  Ingresa PID de proceso a analizar: ")

archivos = []

direccion = "/proc/"+proceso+"/maps"

maps = open(direccion, "r")

for linea in maps:
	linea_separada = linea.split()
	print(linea_separada," Len: ",len(linea_separada))

	paginas = linea_separada[0].split("-")

	permisos = linea_separada[1]

	if(len(linea_separada) == 6):
		ubicacion = linea_separada[5]
	else:
		ubicacion = "Vacio"


	archivos.append([paginas[0][:-3], paginas[1][:-3], permisos, ubicacion])

print("\n\n\n\n LISTA: \n\n")

for p in archivos:
	print("Archivo: ",p)

print("\n\n\n\n LISTA ARREGLADA: \n\n")

for elemento in archivos:

	if(elemento[3][0] == "/"):
	
		if(elemento[3][0:4] == "/lib" or elemento[3][0:8] == "/usr/lib"):
			print("Bib->",end="")

		if(elemento[2][2] == "x"):
			print("Texto  |",end="")
		else:
			print("Datos  |",end="")

	else:
		print(elemento[3],"  |",end="")

	print(elemento[0],elemento[1],"  |",end="")

	paginas = int(elemento[1],16)-int(elemento[0],16)

	print(paginas * 4000," bytes  |", paginas, "  |", elemento[2],"  |", elemento[3], end="")

	print("\n",end="")

