# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 01:08:43 2020

@author: carlos
"""
from random import randint
import math
import copy



NUM_CARGAS=4
NOMBRE_PROCESOS=['A','B','C','D','E','F','G','H']
NUM_COLAS_PRIORIDAD=7
def printLista(l):
    for i in l:
        print(i)


def cargaClase(l):
    l.append([0,3,'A'])
    l.append([1,5,'B'])
    l.append([3,2,'C'])
    l.append([9,5,'D'])
    l.append([12,5,'E'])

def carga(letra):
    return [randint(0,6),randint(4,8),letra]

def fcfs(l):
    c=copy.deepcopy(l)
    T=0.0
    E=0.0
    P=1
    
    c[0].append(c[0][0])
    T=c[0][1]
    
    for i in range (1,NUM_CARGAS):
        te=(c[i-1][3]+c[i-1][1])-c[i][0]
        c[i].append(te+c[i][0])
        E=te+E
        T=T+te+c[i][1]
        
        P=P+(te+c[i][1])/c[i][1]
    E=E/NUM_CARGAS
    T=T/NUM_CARGAS
    P=P/NUM_CARGAS
    print("FCFS: ")
    
    for i in range (0,NUM_CARGAS):
        for x in range(0,c[i][1]):
            print(c[i][2],end='')
    print()
    print("T=%f E=%f P=%f"%(T,E,P))
    print("----------------------")
    

def rr(l,q):
    c=[]
    c=copy.deepcopy(l)
    print("RR%d: "%q)
    queue=[]
    t=c[0][0]
    n=0
    for i in c:
        if i[0]==t:
            c[n].append(0)
            queue.append(i)
        n=n+1
    r=[]
    
    
    todosIniciados=False
    while True:
        for i in range (0,NUM_CARGAS):
            if todosIniciados==True:
                break
            if(c[i][0]<=t+q and c[i].__len__()<4):
                c[i].append(0)
                queue.append(c[i])
                
                if (i==NUM_CARGAS-1):
                    todosIniciados=True
        corteQ=0    
        n=0

        for i in queue:
           if n==0:
               i[1]=i[1]-q
               if i[1]>0:
                   
                   for x in range(0,q):
                       print(i[2],end='')
                       corteQ=corteQ+1
                   
               elif i[1]<=0:
                   for x in range(0,q+i[1]):
                       print(i[2],end='')
                       corteQ=corteQ+1
                   i[1]=0
                   r.append(i)
               n=1
           else:
               queue.remove(i)
               i[3]=i[3]+t+corteQ-i[0]
               
               
               i[0]=i[0]+t+corteQ-i[0]
               
               queue.insert(n,i)
               n=n+1
        
        aux=queue[0]
        queue.remove(aux)
        aux[0]=aux[0]+corteQ
        queue.append(aux)
        
        for i in queue:
            if i[1]==0:
                queue.remove(i)
        
        if todosIniciados==True and queue.__len__()==0:
            print()
            break
        
        t=t+corteQ
    P=0.0
    E=0.0
    T=0.0
    for i in range (0,NUM_CARGAS):
        for j in range(0,NUM_CARGAS):
            if c[i][2]==r[j][2]:
                T=T+l[i][1]+r[j][3]
                E=E+r[j][3]
                P=P+(l[i][1]+r[j][3])/l[i][1]
    E=E/NUM_CARGAS
    T=T/NUM_CARGAS
    P=P/NUM_CARGAS
    
    print("T=%f E=%f P=%f"%(T,E,P))
    print("----------------------")
    
def spn(l):
    print("SPN: ")
    c=copy.deepcopy(l)
    for x in c:
        x.append(0)
        x.append(False)
    queue=[]
    t=c[0][0]
    todosIniciados=False
    while True:    
        for i in range(0,NUM_CARGAS):
            if c[i][0]<=t and c[i][4]==False:
                c[i][4]=True
                c[i][3]=t-c[i][0]
                queue.append(c[i])
                if i==NUM_CARGAS-1:
                    todosIniciados=True
        if queue.__len__()==0:
            continue
        else:
            pivote=queue[0]
        for i in range(0,queue.__len__()):
            if queue[i][1]<pivote[1]:
                pivote=queue[i]
        for i in range(0,pivote[1]):
            print(pivote[2],end='')
        
        queue.remove(pivote)
        t=t+pivote[1]
        for i in range(0,queue.__len__()):
            queue[i][3]=queue[i][3]+pivote[1]
        
        if todosIniciados==True and queue.__len__()==0:
            print()
            break
    
    P=0.0
    E=0.0
    T=0.0    
    for x in c:
        T=T+x[1]+x[3]
        E=E+x[3]
        P=P+(x[1]+x[3])/x[1]
        
    E=E/NUM_CARGAS
    T=T/NUM_CARGAS
    P=P/NUM_CARGAS
    
    print("T=%f E=%f P=%f"%(T,E,P))
    print("----------------------")    

def fb(l,qb,n):
    print("FB: ")
    c=copy.deepcopy(l)
    for x in c:
        x.append(0)
        x.append(False)
        x.append(x[1])
    queue=[]
    for i in range(0,NUM_COLAS_PRIORIDAD):
        queue.append([])
    
    t=c[0][0]
    todosIniciados=False
    while True:
        for i in range(0,NUM_CARGAS):
            if c[i][0]<=t and c[i][4]==False:
                c[i][4]=True
                c[i][3]=t-c[i][0]
                queue[0].append(c[i])
                if i==NUM_CARGAS-1:
                    todosIniciados=True
        tmp=[]
        aux=0
        moveToQ=0
                    
        for i in range(0,NUM_COLAS_PRIORIDAD):
            if queue[i].__len__()==0:
                continue
            Q=fbQ(i,qb)
            queue[i][0][1]=queue[i][0][1]-(Q*n)
            if queue[i][0][1]<=0:
                aux=(Q*n)+queue[i][0][1]
                queue[i][0][1]=0
            else:
                aux=Q*n
            for k in range(0,int(aux)):
                print(queue[i][0][2],end='')                
            tmp=queue[i][0]
            queue[i].remove(tmp)
            moveToQ=i+1
            break
            
        for i in range(0,NUM_COLAS_PRIORIDAD):
            for j in range(0,queue[i].__len__()):
                queue[i][j][3]=queue[i][j][3]+aux
        
        if tmp[1]>0:
            queue[moveToQ].append(tmp)
        t=t+aux   
        
        stop=True
        if todosIniciados==True:
            for i in range(0,NUM_COLAS_PRIORIDAD):
                if queue[i].__len__()>0:
                    stop=False
            if stop==True:
                print()
                break
    
    P=0.0
    E=0.0
    T=0.0    
    for x in c:
        T=T+x[3]+x[5]
        E=E+x[3]
        P=P+(x[3]+x[5])/x[5]
    E=E/NUM_CARGAS
    T=T/NUM_CARGAS
    P=P/NUM_CARGAS
    
    print("T=%f E=%f P=%f"%(T,E,P))
    print("----------------------") 
            
def fbQ(n,q):
    return math.pow(2,n*q)  

print("Inicio del programa")
cargas=[]
print("**************Carga aleatoria 1:****************")
for i in range (0,NUM_CARGAS):
    cargas.append(carga(NOMBRE_PROCESOS[i]))
    print(cargas[i][2]+': '+str(cargas[i][0])+', t='+str(cargas[i][1])+';',end=' ')
print()

cargas.sort()
fcfs(cargas)
rr(cargas,1)
rr(cargas,4)
spn(cargas)
fb(cargas,1,1)
cargas.clear()
print("**************Carga aleatoria 2:****************")
for i in range (0,NUM_CARGAS):
    cargas.append(carga(NOMBRE_PROCESOS[i]))
    print(cargas[i][2]+': '+str(cargas[i][0])+', t='+str(cargas[i][1])+';',end=' ')
print()

cargas.sort()
fcfs(cargas)
rr(cargas,1)
rr(cargas,4)
spn(cargas)
fb(cargas,1,1)
cargas.clear()
print("**************Carga aleatoria 3:****************")
for i in range (0,NUM_CARGAS):
    cargas.append(carga(NOMBRE_PROCESOS[i]))
    print(cargas[i][2]+': '+str(cargas[i][0])+', t='+str(cargas[i][1])+';',end=' ')
print()

cargas.sort()
fcfs(cargas)
rr(cargas,1)
rr(cargas,4)
spn(cargas)
fb(cargas,1,1)
cargas.clear()
print("**************Carga aleatoria 4:****************")
for i in range (0,NUM_CARGAS):
    cargas.append(carga(NOMBRE_PROCESOS[i]))
    print(cargas[i][2]+': '+str(cargas[i][0])+', t='+str(cargas[i][1])+';',end=' ')
print()

cargas.sort()
fcfs(cargas)
rr(cargas,1)
rr(cargas,4)
spn(cargas)
fb(cargas,1,1)
cargas.clear()
print("**************Carga aleatoria 5:****************")
for i in range (0,NUM_CARGAS):
    cargas.append(carga(NOMBRE_PROCESOS[i]))
    print(cargas[i][2]+': '+str(cargas[i][0])+', t='+str(cargas[i][1])+';',end=' ')
print()

cargas.sort()
fcfs(cargas)
rr(cargas,1)
rr(cargas,4)
spn(cargas)
fb(cargas,1,1)
cargas.clear()





