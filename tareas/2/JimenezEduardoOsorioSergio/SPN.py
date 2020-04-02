#!/usr/bin/env python
# coding: utf-8

# In[21]:


def tiempoEspera(procesos, n, tiempoDeEspera,ordenEjecucion):  
    tiempo_restante = [0] * n 
  
    #Copiar el tiempo de procesamiento en tiempo_restante[]  
    for i in range(n):  
        tiempo_restante[i] = procesos[i][1] 
    completados = 0
    t = 0
    minm = 999999999
    masCorto = 0
    done = False
    
    while (completados != n): 
        #Encontrar el proceso que requiera el tiempo minimo
        for j in range(n): 
            if ((procesos[j][2] <= t) and 
                (tiempo_restante[j] < minm) and tiempo_restante[j] > 0): 
                minm = tiempo_restante[j] 
                masCorto = j 
                done = True
        if (done == False): 
            t += 1
            continue

        #Actualiza el tiempo restante
        tiempo_restante[masCorto] -= 1
  
        #Actualiza el minimo  
        minm = tiempo_restante[masCorto]  
        if (minm == 0):  
            minm = 999999999
  
        #Si un proceso se ha completado
        if (tiempo_restante[masCorto] == 0):  
            
            #Completados +1
            completados += 1
            done = False
  
            fint = t + 1
  
            #Calcular tiempo de espera  
            tiempoDeEspera[masCorto] = (fint - proc[masCorto][1] -    
                                proc[masCorto][2]) 
  
            if (tiempoDeEspera[masCorto] < 0): 
                tiempoDeEspera[masCorto] = 0
          
        # Incrementar el tiempo 
        t += 1
        
#Calcular el tiempo de respuesta
def tiempoRespuesta(procesos, n, tiempoDeEspera, tiempoDeRespuesta):  
       
    for i in range(n): 
        tiempoDeRespuesta[i] = procesos[i][1] + tiempoDeEspera[i]  

#Calcular promedios de tiempo de respuesta y de espera
def tiempoPromedio(procesos, n,ordenEjecucion):  
    tiempoDeEspera = [0] * n 
    
    tiempoDeRespuesta = [0] * n  
  
    tiempoEspera(procesos, n, tiempoDeEspera,ordenEjecucion)  
  
    tiempoRespuesta(procesos, n, tiempoDeEspera, tiempoDeRespuesta)  
  
    print("procesos        Tiempo Procesamiento      Tiempo de Espera       Tiempo de Respuesta") 
    total_tiempoDeEspera = 0
    total_tiempoDeRespuesta = 0
    for i in range(n): 
  
        total_tiempoDeEspera = total_tiempoDeEspera + tiempoDeEspera[i]  
        total_tiempoDeRespuesta = total_tiempoDeRespuesta + tiempoDeRespuesta[i]  
        print(" ", procesos[i][0], "\t\t\t", procesos[i][1], "\t\t\t",tiempoDeEspera[i],"\t\t\t", tiempoDeRespuesta[i]) 
  
    print("\nTiempo promedio de espera = %.2f "%(total_tiempoDeEspera /n) ) 
    print("Tiempo promedio de respuesta  = ", total_tiempoDeRespuesta / n)  
       
if __name__ =="__main__": 
    ordenEjecucion=[]
    proc = [[1,6,1],[2,8,1],[3,7,2],[4,3,3]] 
    n = 4
    tiempoPromedio(proc, n,ordenEjecucion) 
 


# In[ ]:




