##################AUXILIAR FUNCTIONS 

from processClass import process
from random import randint


def initProcesss(n):

	#If you want to change any param you can do it here ñ.ñ
	listAux = []
	name = 65

	arriveT  = 0
	workDuration  = 0
	
	max_arriveT  = 15 		#<--
	max_workDuration  = 10  #<--

	#Random data generation

	for i in range (0,n):
		arriveT  = randint(0,max_arriveT )
		workDuration  = randint(1,max_workDuration )
		p = process(arriveT ,workDuration ,chr(name))
		name += 1
		listAux.append(p)

	return listAux

def avgProcess(lista_processs):
	anwsTime = 0
	penalitation = 0 
	sleepT = 0

	for process in lista_processs:
	    process.generalOP()

	    anwsTime += process.anwsTime
	    sleepT += process.sleepT
	    penalitation += process.penalitation

    #Operations
	anwsTime = anwsTime / len(lista_processs)
	penalitation = penalitation / len(lista_processs)
	sleepT = sleepT  / len(lista_processs)

	return f" |  Time:{anwsTime:.3f} | Wait or sleep:{sleepT:.3f} | Penalitation:{penalitation:.3f}"

def arriveProcess(processList, sysTime):
	queue = []
	for process in processList:
		if( process.arriveT  == sysTime):
			queue.append(process)
	return queue


def resetProcess(processList):
	for process1 in processList:
		process1.resetMethod()




