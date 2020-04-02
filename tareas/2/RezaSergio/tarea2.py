import random
from collections import deque
#Estructura de los procesos
class proceso:
	def __init__(self, name, inicio):
		self.name=name
		self.time=self.timeF=random.randrange(3,10)
		self.inicio=inicio
		self.terminado=0
		self.finish=False
		self.realizar=False
	def printName(self):
		return self.name
	def printTime(self):
		return str(self.time)
	def printPrioridad(self):
		return str(self.printPrioridad)


	def printInfo(self):
		print("{}\tInicio: {} Fin: {} T: {}".format(self.name, self.inicio, self.terminado,self.time))
#Impresion de la información del proceso
def printProcesos(lP):
	for pp in lP:
		print(pp.printName() + "\tt:"+pp.printTime())

"""
	Función para los cálculos
	T=tiempo de respuesta
	E=tiempo de espera
	P=Proporcion de penalizacion

"""
def calculos(T,dato):
	T=T-dato.inicio
	E=dato.terminado-dato.inicio-dato.time
	P=T/(dato.terminado-dato.inicio)
	return T,E,P

"""
	Impresión de los procesos realizados
"""
def printTEP(t,p,e,size, processData):
	ttotal=ptotal=etotal=0
	cadenaProc=""
	for ttime in range (size):
		ttotal+=t[ttime]
		ptotal+=p[ttime]
		etotal+=e[ttime]

	ttotal=ttotal/size
	ptotal=ptotal/size
	etotal=etotal/size
	for p in processData:
		cadenaProc+=p
		cadenaProc+='|'
	print (cadenaProc)
	print ('T: {:<5} \t E: {:<5} P: {:<5} '.format(ttotal,etotal,ptotal))

"""Algoritmo FCFS/FIFO"""
def FCFS (listProcesos):
	fcfs=deque()
	processData=[]
	size=0
	T=[]
	P=[]
	E=[]
	timeTotal=0
	for prox in listProcesos:
		fcfs.append(prox)
		T.append(0)
		P.append(0)
		E.append(0)
		prox.finish=False
		prox.realizar=False
		size+=1


	for i in range (size):
		dato=fcfs.popleft()
		
		T[i]=dato.inicio
		time=0
		for t in range (dato.time):
			processData.append(dato.name)
			timeTotal+=1
			time+=1
			T[i]+=1
		dato.finish=True
		dato.terminado=timeTotal
		
		T[i],E[i],P[i]=calculos(T[i],dato)

		#print(str(T[i]) +" "+str(E[i])+" "+str(P[i]))

	print("Proceso FCFS")
	printTEP(T,P,E,size, processData)

"""Algoritmo Robin Round"""
def RoundRobin(listProcesos, quantum):
	roundR=listProcesos.copy()
	processData=[]
	size=0
	T=[]
	P=[]
	E=[]
	time=0
	timeTotal=0
	quantTaken=0
	terminado=False
	cambio=False
	i=0
	for prox in roundR:
		T.append(0)
		P.append(0)
		E.append(0)
		prox.finish=False
		prox.realizar=False
		size+=1
	
	while(terminado==False):
		
		processData.append(roundR[i].name)
		#print(processData)
		timeTotal+=1
		
		roundR[i].timeF=roundR[i].timeF-1
		T[i]+=1
		quantTaken=quantTaken+1
		roundR[i].realizar=True
		j=0
		for time in roundR:

			if(time.inicio<=timeTotal and time.finish==False):
				T[j]+=1
			j+=1

		if(roundR[i].timeF==0):
			#print("Proceso terminado "+roundR[i].name)
			roundR[i].finish=True
			roundR[i].terminado=timeTotal
			T[i],E[i],P[i]=calculos(T[i],roundR[i])

		
		if(quantTaken==quantum):
			#print("Quantum")
			for dato in roundR:
				if(dato.realizar==False and dato.inicio <= timeTotal and cambio==False and dato.timeF!=0  and dato.finish!=True):
					dato.realizar==True
					roundR[i].realizar=False
					i=roundR.index(dato)
					#print("Cambio a "+roundR[i].name)
					cambio=True
					
				#else:
				#	print("Sin Cambio a "+dato.name)
			cambio=False
			quantTaken=0
			#print("2 Cambio a "+roundR[i].name+" Quantum "+str(quantTaken))
			cambio=False
		for temp in roundR:
			
			if(temp.finish!=False):
				terminado=True
			else:
				terminado=False
			
		
	print("Proceso RR Quantum: {}".format(quantum))
	printTEP(T,P,E,size, processData)

"""Algoritmo SPN"""
def SPN (listProcesos):
	listSPN=listProcesos.copy()
	processData=[]
	size=0
	T=[]
	P=[]
	E=[]
	time=0
	timeTotal=0
	terminado=0
	timeTotal=0
	fin=0
	tiempo_Request=0

	for prox in listSPN:
		
		T.append(0)
		P.append(0)
		E.append(0)
		prox.finish=False
		prox.realizar=False
		size+=1
	
	i=0
	while(fin!=size):
		
		
		
		
		for t in range (listSPN[i].time):
			processData.append(listSPN[i].name)
			timeTotal+=1
			
			T[i]+=1
		listSPN[i].finish=True
		listSPN[i].terminado=timeTotal
		fin+=1
		#print("Termino proceso "+listSPN[i].name)
		T[i],E[i],P[i]=calculos(T[i],listSPN[i])
		tiempo_Request=0
		for j in range(size):
			
			if (listSPN[j].finish!=True and listSPN[j].inicio<=timeTotal):
				if(tiempo_Request==0 or tiempo_Request>=listSPN[j].time):
					#print("Oportunidad a "+listSPN[j].name)
					tiempo_Request=listSPN[j].time
					i=j
			

		
			

		#print(str(T[i]) +" "+str(E[i])+" "+str(P[i]))

	print("Proceso SPN")
	printTEP(T,P,E,size, processData)






#Creacion de procesos
procesoA= proceso('A',0)
procesoB= proceso('B',1)
procesoC= proceso('C',3)
procesoD= proceso('D',9)
procesoE= proceso('E',12)

process=[procesoA, procesoB, procesoC, procesoD, procesoE]
processFCFS= process.copy()
processRobinRound=process.copy()
processSPN=process.copy()
print("Comparacion de planificadores")
print ("Procesos Ronda 1 \n")

printProcesos(processFCFS)
FCFS(processFCFS)
RoundRobin(processRobinRound,1)
SPN(processSPN)







