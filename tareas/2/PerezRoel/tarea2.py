#Tarea 2
#de Roel Perez

from random import randint
"""
Genera la tabla de procesos aleatoria. Recibe una lista vacia 'procesos' y
la convierte en una lista de listas de procesos
	
Lista proceso:	[<tiempo de llegada>,<tiempo requerido>,<nombre(caracter)>,
				<tiempo de respuesta>,<tiempo en espera>,<proporcion de penalizacion>,
				<texto de ejecucion>]

Cada tick (t), hay una probabilidad de 1/p de que llegue un proceso con un tiempo
requerido entre tmin y tmax. T,E,P se inicializan en 0. 
"""
def generarProcesos(procesos,n,p,tmin,tmax):
	t = 0
	nombreASCII = 65 
	while(n > 0):
		if(randint(0,p-1) == 0):
			proceso = [t,randint(tmin,tmax),chr(nombreASCII),0,0,0,""]
			procesos.append(proceso)
			nombreASCII += 1
			n -= 1
		t += 1

"""
Calcula los E y P de cada proceso en lista_tareas
"""
def resultados(lista_tareas):
	for i in lista_tareas:
		i[4] = i[3] - i[1]
		i[5] = i[3] / i[1]

"""
Calcula los promedios T, E y P en lista_tareas.
Recibe una lista con la forma [0,0,0] y almacena ahi los promedios.
"""
def promedios(lista_tareas, promedios):
	for i in lista_tareas:
		promedios[0] += i[3]
		promedios[1] += i[4]
		promedios[2] += i[5]
	for i in range(len(promedios)):
		promedios[i] = promedios[i]/len(lista_tareas)

"""
Muestra la tabla con el nombre, t, tiempo de inicio, tiempo de fin, T, E y P de cada proceso en lista_tareas.
"""
def tabla(lista_tareas,algoritmo):
	print("\n"+algoritmo)
	prom = [0,0,0]
	promedios(lista_tareas,prom)
	print('Proceso\tt\tInicio\tFin\tT\tE\tP')
	for i in lista_tareas:
		print(i[2]+"\t"+str(i[1])+"\t"+str(i[0])+"\t"+str(i[0]+i[3])+"\t"+str(i[3])+"\t"+str(i[4])+"\t"+str(i[5]))
	print("Promedio:\t\t\tT="+str(prom[0])+"\t"+"E="+str(prom[1])+"\t"+"P="+str(prom[2]))

"""
Muestra el diagrama donde se observan los procesos, desde su inicio hasta su fin. 
"""
def diagrama(lista_tareas):
	print("\nDiagrama: ")
	for i in lista_tareas:
		print((" "*i[0]) + i[6])


#FIRST COME FIRST SERVE
def fcfs(tareas):
	tareas_ent = []
	for i in tareas:
		tareas_ent.append(i.copy())
	t = 0
	esquema = ""
	tareas_cola = []
	tareas_ent_ite = 0
	tareas_cola_ite = 0

	#Mientras haya procesos pendientes, de entrada o en la cola
	while(tareas_ent_ite < len(tareas_ent) or len(tareas_cola) != 0):

		#Si es el tiempo de llegada de un proceso, se agrega a la cola
		if(tareas_ent_ite < len(tareas_ent)):
			if(tareas_ent[tareas_ent_ite][0] == t):
				tareas_cola.append(tareas_ent[tareas_ent_ite].copy())
				tareas_ent_ite += 1

		#Si hay procesos en la cola
		if(len(tareas_cola) > 0):
			esquema = esquema + tareas_cola[0][2] 
			for i in tareas_cola:
				i[3]+=1
			tareas_cola[0][1] -= 1
			######
			tareas_cola[0][6] = tareas_cola[0][6] + tareas_cola[0][2]
			for i in range (1, len(tareas_cola)):
				tareas_cola[i][6] = tareas_cola[i][6] + '-'
			######
			if(tareas_cola[0][1] == 0):
				tareas_ent[tareas_cola_ite][3] = tareas_cola[0][3]
				tareas_ent[tareas_cola_ite][6] = tareas_cola[0][6] ######
				tareas_cola_ite += 1;
				tareas_cola.pop(0) 
		else:
			esquema = esquema + "i"

		t = t+1

	resultados(tareas_ent)
	tabla(tareas_ent,"FCFS")
	diagrama(tareas_ent)
	print("ESQUEMA:")
	print(esquema)


#ROUND ROBIN
#Se recibe el tamanio del Quantum como n
def rrn(tareas, n):
	tareas_ent = []
	for i in tareas:
		tareas_ent.append(i.copy())
	t = 0
	esquema = ""
	tareas_cola = []
	tareas_ent_ite = 0
	quantum = n
	encolar = None

	#Mientras haya procesos pendientes, de entrada o en la cola
	while(tareas_ent_ite < len(tareas_ent) or len(tareas_cola) != 0 or encolar != None):

		#Si es el tiempo de llegada de un proceso, agregarlo a la cola
		if(tareas_ent_ite < len(tareas_ent)):
			if(tareas_ent[tareas_ent_ite][0] == t):
				tareas_cola.append(tareas_ent[tareas_ent_ite].copy())
				tareas_ent_ite += 1

		#Ultimo proceso en ejecutar que no termino y debe encolarse hasta el final
		if(encolar != None ):
			tareas_cola.append(encolar)
			encolar = None

		#Si hay procesos en la cola
		if(len(tareas_cola) > 0):
			esquema = esquema + tareas_cola[0][2]
			for i in tareas_cola:
				i[3]+=1 
			tareas_cola[0][1] -= 1
			quantum -= 1

			######
			tareas_cola[0][6] = tareas_cola[0][6] + tareas_cola[0][2]
			for i in range (1, len(tareas_cola)):
				tareas_cola[i][6] = tareas_cola[i][6] + '-'
			######

			if(tareas_cola[0][1] == 0):
				nombre = tareas_cola[0][2]
				for i in range(len(tareas_ent)):
					if(tareas_ent[i][2] == nombre):
						tareas_ent[i][3] = tareas_cola[0][3]
						tareas_ent[i][6] = tareas_cola[0][6] #####
						break
				tareas_cola.pop(0)
				quantum = n 
			elif(quantum == 0):
				encolar = tareas_cola.pop(0)
				quantum = n
		else:
			esquema = esquema + "i"

		t = t+1

	resultados(tareas_ent)
	tabla(tareas_ent,"RR"+str(n))
	diagrama(tareas_ent)
	print("\nESQUEMA:")
	print(esquema)

#SHORTEST PROCESS NEXT
#Se reciben la tabla de tareas
def spn(tareas):
	tareas_ent = []
	for i in tareas:
		tareas_ent.append(i.copy())
	t = 0
	esquema = ""
	tareas_cola = []
	tareas_ent_ite = 0
	ejec = 0

	#Mientras no haya procesos pendientes, ni de entrada ni en la cola
	while(tareas_ent_ite < len(tareas_ent) or len(tareas_cola) != 0):

		#Si es el tiempo de llegada de un proceso, pone en la parte correcta de la cola
		if(tareas_ent_ite < len(tareas_ent)):
			if(tareas_ent[tareas_ent_ite][0] == t):
				p = ejec
				for i in range(ejec,len(tareas_cola)):
					if(tareas_ent[tareas_ent_ite][1] < tareas_cola[i][1]):
						p = i
						break
					p+=1
				tareas_cola.insert(p,tareas_ent[tareas_ent_ite].copy())
				tareas_ent_ite += 1

		#Si hay procesos en la cola
		if(len(tareas_cola) > 0):
			esquema = esquema + tareas_cola[0][2]
			for i in tareas_cola:
				i[3]+=1 
			tareas_cola[0][1] -= 1

			######
			tareas_cola[0][6] = tareas_cola[0][6] + tareas_cola[0][2]
			for i in range (1, len(tareas_cola)):
				tareas_cola[i][6] = tareas_cola[i][6] + '-'
			######

			ejec = 1
			if(tareas_cola[0][1] == 0):
				nombre = tareas_cola[0][2]
				for i in range(len(tareas_ent)):
					if(tareas_ent[i][2] == nombre):
						tareas_ent[i][3] = tareas_cola[0][3]
						tareas_ent[i][6] = tareas_cola[0][6] #####
						break
				tareas_cola.pop(0)
				ejec = 0
		else:
			esquema = esquema + "i"
		t = t+1

	resultados(tareas_ent)
	tabla(tareas_ent,"SPN")
	diagrama(tareas_ent)
	print("\nESQUEMA:")
	print(esquema)


#RONDA EGOISTA
#se reciben la tabla de tareas, y el valor deseado para a y b
def srr(tareas,a,b):
	tareas_ent = []
	for i in tareas:
		tareas_ent.append(i.copy())
	for i in tareas_ent:
		i[4] = a 
	t = 0
	esquema = ""
	tareas_colas = []
	tareas_ent_ite = 0

	#Mientras no haya procesos pendientes, ni de entrada ni en la cola
	while(tareas_ent_ite < len(tareas_ent) or len(tareas_colas) != 0):

		#Se obtienen los procesos entrantes, y se colocan en la cola 0
		if(tareas_ent_ite < len(tareas_ent)):
			if(tareas_ent[tareas_ent_ite][0] == t):
				if(len(tareas_colas) == 0):
					tareas_colas.append([])
				tareas_colas[0].append(tareas_ent[tareas_ent_ite].copy())
				tareas_ent_ite += 1

		if(len(tareas_colas) > 0): 
			#Se busca el proceso con mayor prioridad en las colas y se ejecuta
			sigEjec = tareas_colas[len(tareas_colas)-1].pop(0)
			sigEjec[4] = b
			esquema = esquema + sigEjec[2]
			sigEjec[1] -= 1
			####
			sigEjec[6] = sigEjec[6] + sigEjec[2]
			for i in tareas_colas:
				for j in i:
					j[6] = j[6] + '-'
			####
			#Se vuelve a encolar si no ha terminado; de lo contrario, devuelve su info a la cola entrante
			if(sigEjec[1] > 0):
				tareas_colas[len(tareas_colas)-1].insert(0,sigEjec)
			else:
				nombre = sigEjec[2]
				sigEjec[3] += 1
				for i in range(len(tareas_ent)):
					if(tareas_ent[i][2] == nombre):
						tareas_ent[i][3] = sigEjec[3]
						tareas_ent[i][6] = sigEjec[6] #####
						break
			#Se actualiza la prioridad de todos los procesos
			for i in reversed(range(0,len(tareas_colas))):
				for j in range(0,len(tareas_colas[i])):
					p = tareas_colas[i].pop(0)
					p[3] += 1
					if(len(tareas_colas) < i+1+p[4]):
						for k in range(0,p[4]):
							tareas_colas.append([])
					tareas_colas[i+p[4]].insert(0,p)
			#Se borran las colas innecesarias
			ultima = 0
			for i in reversed(range(0,len(tareas_colas))):
				if (len(tareas_colas[i]) != 0):
					ultima = i+1
					break
			for i in range(ultima,len(tareas_colas)):
				tareas_colas.pop(ultima)
		else:
			esquema = esquema + "i"

		t += 1
	
	resultados(tareas_ent)
	tabla(tareas_ent,"SRR")
	diagrama(tareas_ent)
	print("\nESQUEMA:")
	print(esquema)

tareas1 = []
generarProcesos(tareas1,5,3,3,12)

fcfs(tareas1)
rrn(tareas1,1)
rrn(tareas1,4)
spn(tareas1)
srr(tareas1,2,1)
""""
print("\n***************************************************")

tareas2 = []
generarProcesos(tareas2,5,3,3,12)

fcfs(tareas2)
rrn(tareas2,1)
rrn(tareas2,4)
spn(tareas2)
srr(tareas2,2,1)

print("\n***************************************************")

tareas3 = []
generarProcesos(tareas3,5,5,3,12)

fcfs(tareas3)
rrn(tareas3,1)
rrn(tareas3,4)
spn(tareas3)
srr(tareas3,2,1)
"""