#!/usr/bin/env python
# coding: utf-8

# In[69]:


import numpy as np
import random
              
#Calcular tiempo promedio de espera y promedio de respuesta
def promedioTiempos(proceso, n,tiempoProcesamiento, quantum,ordenEjecucion):  
    TE = [0] * n 
    tiempoDeRespuesta = [0] * n  
    
    tiempoEspera(proceso, n,tiempoProcesamiento,  TE, quantum,ordenEjecucion)  

    tiempoRespuesta(proceso, n,tiempoProcesamiento, TE, tiempoDeRespuesta)  
  
    print("proceso      Tiempo procesamiento       Tiempo de Espera      Tiempo de respuesta") 
    total_TE = 0
    total_tiempoDeRespuesta = 0
    for i in range(n): 
  
        total_TE = total_TE + TE[i]  
        total_tiempoDeRespuesta = total_tiempoDeRespuesta + tiempoDeRespuesta[i]  
        print(" ", i + 1, "\t\t\t",tiempoProcesamiento[i],"\t\t\t", TE[i],"\t\t\t", tiempoDeRespuesta[i]) 
  
    print("\nPromedio de espera = %.2f "%(total_TE /n) ) 
    print("Tiempo promedio de respuesta = %.2f "% (total_tiempoDeRespuesta / n))  
     
#Calcula el tiempo de respuesta
def tiempoRespuesta(proceso, n, tiempoProcesamiento, TE, tiempoDeRespuesta): 
        
    for i in range(n): 
        tiempoDeRespuesta[i] =tiempoProcesamiento[i] + TE[i]  

#Funcion para encontra el tiempo de espera de todos los procesos
def tiempoEspera(proceso, n,tiempoProcesamiento, TE, quantum,ordenEjecucion):  

    TiemProc_restante = [0] * n 
    #Asignar el tiempo de procesamiento a TiempoProc_restante[]  
    for i in range(n):  
        TiemProc_restante[i] =tiempoProcesamiento[i]
    ordenEjecucion.append(TiemProc_restante[i])
    t = 0 # Tiempo t  
    #Ejecuta los procesos en RoundRobin hasta que todos esten terminados
    while(1): 
        done = True
        for i in range(n):
            ordenEjecucion.append(i)
            #IF tiempo de procesamiento es mayor >0 aun necesita procesar mas
            if (TiemProc_restante[i] > 0) : 
                done = False #Aun hay un proceso pendiente
                  
                if (TiemProc_restante[i] > quantum) : 
                
                    #Añade el tiempo de procesamiento que llevamos a t
                    t += quantum  
  
                    #Actualiza el tiempo restante
                    TiemProc_restante[i] -= quantum  
                  
                #Si el tiempo de procesamiento restante es menor a un quantum, solo queda 1 ciclo mas
                else: 
                  
                    #Añade el tiempo de procesamiento que llevamos a t
                    t = t + TiemProc_restante[i]  
                    
                    #Tiempo de Espera
                    TE[i] = t -tiempoProcesamiento[i]  
  
                    #Una vez terminados los procesos 
                    #TiemProc_restante debe ser  0
                    TiemProc_restante[i] = 0
                  
        # Si todos los procesos están terminados  
        if (done == True): 
            break

#Main
if __name__ =="__main__": 
      
    # ID de los procesos
    
    proc = [1,2,3,4] 
    n = 4
    ordenEjecucion=[]
    tiempo_procesamiento=[]
    # Tiempo de procesamiento de los procesos
    for i in range(20):
        tiempo_procesamiento.append(random.randint(1,5))
    # Time quantum  
    quantum = 4;  
    promedioTiempos(proc, n, tiempo_procesamiento, quantum,ordenEjecucion)
    for i in ordenEjecucion:
        if i==0:
            print("A",end = ' ')
        elif i==1:
            print("B",end = ' ')
        elif i==2:
            print("C",end = ' ')
        elif i==3:
            print("D",end = ' ')
 


# In[ ]:




