import random 

class process:
	launchTime=None
	firstProcess=False
	endTime=None
	wait=None
	TotalTime=None
	PTime=None
	def __init__(self, name):
		self.timeToComplete=random.randrange(1,10) #Gets an random amount of the needed time to complete its execution. 
		self.name=name #saves the assigned name. 



ListOfProcess=[]
ListOfProcess.append(process('A'))
ListOfProcess.append(process('B'))
ListOfProcess.append(process('C'))
ListOfProcess.append(process('D'))
ListOfProcess.append(process('E'))

TotalTime=0

#Computes Total time needed 
for obj in ListOfProcess:
	TotalTime=TotalTime+obj.timeToComplete


print('The total time for all processes is %d '%(TotalTime))

# Set the first process
ZeroProcess=ListOfProcess.pop(random.randrange(len(ListOfProcess)))
ZeroProcess.launchTime=0
ZeroProcess.firstProcess=True
ZeroProcess.endTime=ZeroProcess.timeToComplete
ZeroProcess.wait=0
ZeroProcess.TotalTime=ZeroProcess.endTime
ZeroProcess.PTime=1


queue=[] #Queue of execution. 

queue.append(ZeroProcess)

while len(ListOfProcess)>0:
	queue.append(ListOfProcess.pop(random.randrange(len(ListOfProcess))))

for i in range(1,len(queue)):
	previousLT=queue[i-1].launchTime
	previousED=queue[i-1].endTime
	startTime=random.randrange(previousLT,previousED)
	queue[i].launchTime=startTime
	waitingTime=previousED-startTime
	queue[i].wait=waitingTime
	queue[i].endTime=queue[i].launchTime+waitingTime+queue[i].timeToComplete
	queue[i].TotalTime=queue[i].wait+queue[i].timeToComplete
	queue[i].PTime=queue[i].TotalTime/queue[i].timeToComplete

	


averageTime=0
averageWait=0
averagePTime=0

for obj in queue:
	averageTime=averageTime+obj.TotalTime
	averageWait=averageTime+obj.wait
	averagePTime=averageTime+obj.PTime


averageTime=averageTime/(len(queue))
averageWait=averageWait/(len(queue))
averagePTime=averagePTime/(len(queue))

print('FCFS: T=%f, E=%f, P=%f'%(averageTime,averageWait,averagePTime))

for obj in queue:
	for i in range(0,obj.timeToComplete):
		print(obj.name, end = '')

print('')






