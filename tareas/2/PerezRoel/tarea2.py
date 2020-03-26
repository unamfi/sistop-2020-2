#Tarea 2
#de Roel Perez

from random import randint

def resultados(lista_tareas):
	for i in lista_tareas:
		i[4] = i[3] - i[1]
		i[5] = i[3]/i[1]

def promedios(lista_tareas, promedios):
	for i in lista_tareas:
		promedios[0] += i[3]
		promedios[1] += i[4]
		promedios[2] += i[5]
	for i in range(len(promedios)):
		promedios[i] = promedios[i]/len(lista_tareas)

def fcfs(tareas):
	tareas_ent = []
	for i in tareas:
		tareas_ent.append(i.copy())
	t = 0
	esquema = ""
	tareas_cola = []
	tareas_ent_ite = 0
	tareas_cola_ite = 0
	prom = [0,0,0]
	while(tareas_ent_ite < len(tareas_ent) or len(tareas_cola) != 0):

		if(tareas_ent_ite < len(tareas_ent)):
			if(tareas_ent[tareas_ent_ite][0] == t):
				tareas_cola.append(tareas_ent[tareas_ent_ite].copy())
				tareas_ent_ite += 1


		if(len(tareas_cola) > 0):
			esquema = esquema + tareas_cola[0][2]
			for i in tareas_cola:
				i[3]+=1 
			tareas_cola[0][1] -= 1
			if(tareas_cola[0][1] == 0):
				tareas_ent[tareas_cola_ite][3] = tareas_cola[0][3]
				tareas_cola_ite += 1;
				tareas_cola.pop(0) 
		else:
			esquema = esquema + "i"
		t = t+1

	resultados(tareas_ent)
	promedios(tareas_ent, prom)
	print("FCFS: T="+str(prom[0])+", E="+str(prom[1])+", P="+str(prom[2]))
	print(esquema)


def rrn(tareas, n):
	tareas_ent = []
	for i in tareas:
		tareas_ent.append(i.copy())
	t = 0
	esquema = ""
	tareas_cola = []
	tareas_ent_ite = 0
	prom = [0,0,0]
	quantum = n
	encolar = None
	while(tareas_ent_ite < len(tareas_ent) or len(tareas_cola) != 0 or encolar != None):

		if(tareas_ent_ite < len(tareas_ent)):
			if(tareas_ent[tareas_ent_ite][0] == t):
				tareas_cola.append(tareas_ent[tareas_ent_ite].copy())
				tareas_ent_ite += 1

		if(encolar != None ):
			tareas_cola.append(encolar)
			encolar = None

		if(len(tareas_cola) > 0):
			esquema = esquema + tareas_cola[0][2]
			for i in tareas_cola:
				i[3]+=1 
			tareas_cola[0][1] -= 1
			quantum -= 1

			if(tareas_cola[0][1] == 0):
				nombre = tareas_cola[0][2]
				for i in range(len(tareas_ent)):
					if(tareas_ent[i][2] == nombre):
						tareas_ent[i][3] = tareas_cola[0][3]
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
	promedios(tareas_ent,prom)
	print("RR"+str(n)+": T="+str(prom[0])+", E="+str(prom[1])+", P="+str(prom[2]))
	print(esquema)


def spn(tareas):
	tareas_ent = []
	for i in tareas:
		tareas_ent.append(i.copy())
	t = 0
	esquema = ""
	tareas_cola = []
	tareas_ent_ite = 0
	prom = [0,0,0]
	ejec = 0
	while(tareas_ent_ite < len(tareas_ent) or len(tareas_cola) != 0):

		if(tareas_ent_ite < len(tareas_ent)):
			if(tareas_ent[tareas_ent_ite][0] == t):
				p = ejec
				for i in range(ejec,len(tareas_cola)):
					if(tareas_ent[tareas_ent_ite][1] > tareas_cola[i][1]):
						p = i
						break
				tareas_cola.insert(p,tareas_ent[tareas_ent_ite].copy())
				tareas_ent_ite += 1

		if(len(tareas_cola) > 0):
			esquema = esquema + tareas_cola[0][2]
			for i in tareas_cola:
				i[3]+=1 
			tareas_cola[0][1] -= 1
			ejec = 1
			if(tareas_cola[0][1] == 0):
				nombre = tareas_cola[0][2]
				for i in range(len(tareas_ent)):
					if(tareas_ent[i][2] == nombre):
						tareas_ent[i][3] = tareas_cola[0][3]
						break
				tareas_cola.pop(0)
				ejec = 0
		else:
			esquema = esquema + "i"
		t = t+1

	resultados(tareas_ent)
	promedios(tareas_ent, prom)
	print("SPN: T="+str(prom[0])+", E="+str(prom[1])+", P="+str(prom[2]))
	print(esquema)



tareas = []

tareas.append([0,3,"A",0,0,0])
tareas.append([1,5,"B",0,0,0])
tareas.append([3,2,"C",0,0,0])
tareas.append([9,5,"D",0,0,0])
tareas.append([12,5,"E",0,0,0])



fcfs(tareas)

rrn(tareas,1)

rrn(tareas,4)

spn(tareas)