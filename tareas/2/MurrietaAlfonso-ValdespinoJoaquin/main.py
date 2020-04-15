################## MAIN CODE, just for testing 

from processClass import *
from auxFunctions import resetProcess, initProcesss
from process import *

def testFunction():
    lista = []
    p1 = process(0,3,"A")
    p2 = process(1,5,"B")
    p3 = process(3,2,"C")
    p4 = process(9,5,"D")
    p5 = process(12,5,"E")
    lista.append(p1)
    lista.append(p2)
    lista.append(p3)
    lista.append(p4)
    lista.append(p5)
    return lista


lista_cuantums = []
auxNum = int(input("Number of cuantums for RoundRobin: "))
i = 1
while i <= auxNum:
    cuantum = int(input("Insert the cuantum: "))
    lista_cuantums.append(cuantum)
    i += 1


rondas = int(input("Insert number of rounds: "))


for i in range(1,rondas+1):
	lista = initProcesss(3)

	print("\n###########[ROUND "+str(i)+" ]############\n")
	for proceso in lista:
		proceso.printProcess()
	print(" ")

	FCFSprocess(lista)
	resetProcess(lista)

	for j in range(0,len(lista_cuantums)):
		RRprocess(lista,lista_cuantums[j])
		resetProcess(lista)

	SPNprocess(lista)