from random import randint
import time
import copy

procesos_activos = []

procesos=[
    ['A',0,3],
    ['B',1,5],
    ['C',3,2],
    ['D',9,5],
    ['E',12,5]
    ]

alfabeto_procesos = ['A','B','C','D','E']

def generar_carga():
    procesos.clear()
    cuenta=0
    for i in range(0,5):
        procesos.append([alfabeto_procesos[i],cuenta,randint(2,9)])
        cuenta+=randint(2,7)

def fifo():
    i_proceso = 0
    i_tick = 0
    diferencia=0
    recorrido=0
    Tp=Ep=Pp=0
    
    for i_proceso in range(0,5):
        while (i_tick < recorrido+procesos[i_proceso][2]):
            print(" ",procesos[i_proceso][0],end="")
            i_tick+=1

        T=(i_tick-recorrido)+(recorrido-procesos[i_proceso][1])
        E=recorrido-procesos[i_proceso][1]
        P=T/procesos[i_proceso][2]
        print("\n\n ---- Para ",procesos[i_proceso][0],":  T = ",T,"  E = ",E,"  P = ",P)
        recorrido=i_tick
        Tp+=T
        Ep+=E
        Pp+=P

    print("\n T promedio = ",Tp/5,"  E promedio = ",Ep/5,"  P promedio = ",Pp/5)


def round_robin(quantum):
    i_proceso = 0
    i_tick = 0
    diferencia=0
    recorrido=0
    Tp=Ep=Pp=0
    T=E=P= 0

    procesos_no_terminados=copy.deepcopy(procesos)

    #print("LEN DE PRO: ",len(procesos))
        
    
    while(len(procesos_no_terminados)!=0):
        while (i_tick < recorrido+quantum):
            print(" ",procesos_no_terminados[i_proceso][0],end="")
            i_tick+=1
            procesos_no_terminados[i_proceso][2]-=1
            if(procesos_no_terminados[i_proceso][2]==0):
                T=(i_tick-recorrido)+(recorrido-procesos_no_terminados[i_proceso][1])
                E=recorrido-procesos_no_terminados[i_proceso][1]
                P=T/procesos[i_proceso][2]
                
                

                print("\n\n ---- Para",procesos_no_terminados[i_proceso][0],":  T = ",T,"  E = ",E,"  P = ",P)
                procesos_no_terminados.pop(i_proceso)
                
                break
        print("\n")

        while True:
            if i_proceso<len(procesos_no_terminados):
                i_proceso+=1
            else:
                i_proceso=0
            if (i_proceso>=len(procesos_no_terminados)):
                i_proceso=0
                break
            
            if (procesos_no_terminados[i_proceso][1]<=i_tick):
                break

        recorrido=i_tick
        Tp+=T
        Ep+=E
        Pp+=P
        
    print("\n  T promedio = ",Tp/5,"  E promedio = ",Ep/5,"  P promedio = ",Pp/5)
        
    
for i in range(1,6):
	generar_carga()

	print("\n\n\nRonda ",i,"\n\n Procesos: ",procesos,"\n\n")

	print("FCFS: \n")
	fifo()
	print("\n\n ROBIN CON QUANTUM 2: \n")
	round_robin(2)
	print("\n\n ROBIN CON QUANTUM 4: \n")
	round_robin(4)




    
    
    






    

