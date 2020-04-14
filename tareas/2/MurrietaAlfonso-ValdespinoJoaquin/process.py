################## RR, FCFS, SPN process FUNCTIONS 

from processClass import process
from auxFunctions import avgProcess, arriveProcess

################## Round Robin
def RRprocess(processList, cuantumAux):
	print("\nPROCESS: RR - ROUND ROBIN "+ str(cuantumAux)+ "\n")

	sysTime = 0
	processNum = len(processList)
	currentProcess = None
	processQueue = []
	quantumMax = cuantumAux # Ticks number
	quantum = 0

	while(processNum != 0):
		arriveQueue = arriveProcess(processList, sysTime)

		#When the first process arrives, it 'll be added to the queue working and it 'll be executed 
		if(len(arriveQueue) != 0):
			if(len(processQueue)==0):
				p = arriveQueue.pop(0)
				processQueue.append(p)
				currentProcess = processQueue[0]
				currentProcess.working = True
				quantum = 0

				for p in arriveQueue:
					processQueue.append(p)
			else:
				for p in arriveQueue:
					processQueue.append(p)

		if(len(processQueue) != 0 ):

			#Remember that quantum needs to change 
			if(quantum == quantumMax):
				currentProcess.working = False
				quantum = 0

				if(currentProcess.dead == False):
					processQueue.append(currentProcess)
					processQueue.pop(0)

				if(len(processQueue) != 0):
					currentProcess = processQueue[0]
					currentProcess.working = True    
			
			for proceso in processQueue:
				proceso.isWorking()
			quantum += 1

		#MORTAL LINES :( ->  If a process is done (dead) pass to the next one in the queue -> we need to put quartum on zero
			if(currentProcess.dead == True):
				processQueue.pop(0)
				processNum -= 1
				quantum = 0
				if(len(processQueue) != 0):
					currentProcess = processQueue[0]
					currentProcess.working = True

		sysTime += 1

	dataRR = avgProcess(processList)
	print("")
	print(dataRR)


################## First Come First Serve

def FCFSprocess(processList):
	print("\nPROCESS: FCFS - First Come First Serve \n")

	sysTime= 0
	processNum = len(processList)
	currentProcess = None
	processQueue = []

	while(processNum != 0):
		arriveQueue = arriveProcess(processList, sysTime)


		if(len(arriveQueue) != 0):
			if(len(processQueue) == 0):
				p = arriveQueue.pop(0)
				processQueue.append(p)
				currentProcess = processQueue[0]
				currentProcess.working = True
				for p in arriveQueue:
					processQueue.append(p)

			else:
				for p in arriveQueue:
					processQueue.append(p)

		if(len(processQueue) != 0 ):
            #All the process are working, if not just sleep
			for proceso in processQueue:
				proceso.isWorking()

			# If a process is done (dead) pass to the next one in the queue
			if(currentProcess.dead == True):
				processQueue.pop(0)
				processNum -= 1
				if(len(processQueue) != 0):
					currentProcess = processQueue[0]
					currentProcess.working = True
        
		sysTime+= 1

	dataRR = avgProcess(processList)
	print("")
	print(dataRR)



################## Shortest Process Next


def SPNprocess(processList):
	print("\nPROCESS: SPN - Shortest Process Next \n")

	sysTime= 0
	processNum = len(processList)
	currentProcess = None
	processQueue = []
	
	def nearNext(processQueue):
		min = processQueue[0].workDuration
		index = 0
		for i in range(0,len(processQueue) ):
			if(processQueue[i].workDuration<= min):
				min = processQueue[i].workDuration
				index = i
		return index

	while(processNum != 0):
		arriveQueue = arriveProcess(processList, sysTime)

		if(len(arriveQueue) != 0):
			if(len(processQueue) == 0):
				p = arriveQueue.pop(0)
				processQueue.append(p)
				currentProcess = processQueue[0]
				currentProcess.working = True
				for p in arriveQueue:
					processQueue.append(p)
			else:
				for p in arriveQueue:
					processQueue.append(p)

		if(len(processQueue) != 0 ):
			if(currentProcess == None):
				index = nearNext(processQueue)
				currentProcess = processQueue[index]
				processQueue.pop(index)
				processQueue.insert(0,currentProcess)
				currentProcess.working = True

			# Se ponen a isWorkingr a todos los procesos, en caso de no tener la working, estos descansan
			for proceso in processQueue:
				proceso.isWorking()

			# Si el proceso en working ya acabo se le cede la working al siguente proceso en la cola
			if(currentProcess.dead == True):
				processQueue.pop(0)
				processNum -= 1
				currentProcess = None
		sysTime+= 1


	dataRR = avgProcess(processList)
	print("")
	print(dataRR)









