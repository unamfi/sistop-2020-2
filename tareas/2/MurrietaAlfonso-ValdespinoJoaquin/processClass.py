##################PROCESS CLASS

#As we well know, all processes have things in common, 
# that is why we decided to generalize these properties in a class

class process():

	def __init__(self, arriveT , workDuration , name):
			
			self.name = name
			self.dead = False
			self.working = False # It is n't the same the state that the time of state<- This is the state
			
			self.arriveT  = arriveT 
			self.workingT  = 0
			self.sleepT = 0

			self.workLong  = workDuration 
			self.workDuration  = workDuration 

			
			
	#NOTA EXPRESS: Posteriormente encontramos que hay métodos de bajo nivel de objetos que hacen esto :(
	def resetMethod(self):
		
		self.name = self.name
		self.dead = False
		self.working = False

		self.arriveT  = self.arriveT 
		self.workingT  = 0
		self.sleepT = 0

		self.workLong  = self.workDuration 
		self.workDuration  = self.workDuration 
		

	def isWorking(self):
		if(not self.dead and self.working):
			self.workingT  += 1
			self.workLong  -= 1

			print(self.name,end="")

			if(self.workLong  == 0):
				self.dead = True
		else:
			self.sleepT += 1

	#Calculations and operations methods

	def anwsTimeOP(self):
		self.anwsTime = self.workingT + self.sleepT

	def anwsOP(self):
		self.porAnws = self.workingT/self.anwsTime

	def penalitationOP(self):
		self.penalitation = self.anwsTime/self.workingT

	def generalOP(self):
		self.anwsTimeOP()
		self.anwsOP()
		self.penalitationOP()

	def printProcess(self):
		print(f"{self.name}:{self.arriveT }, t:{self.workDuration }",end=" ")
