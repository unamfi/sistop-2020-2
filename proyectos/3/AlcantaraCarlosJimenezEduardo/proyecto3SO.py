# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math

#Funcion que resta dos numeros hexadecimales y regresa el resultado en hexadecimal
def restaHex(a,b):
    numA=int(a,16)
    numB=int(b,16)
    return hex(numA-numB)

#Toma un renglon de datos, y regresa su direccion de comienzo
def retDirA(row):
    d=row[0].split('-')
    return d[0]

#Toma un renglon de datos, y regresa su direccion de termino
def retDirB(row):
    d=row[0].split('-')
    return d[1]

#Regresa true si encontro la coincidencia character en la palabra word
def exist(word,character):
    compare=word.find(character)
    if compare!=-1:
        return True
    else:
        return False

#Usado para imprimir los datos con formato
def printFormat(row):
    print("|%10s |%9s|%9s| %25s | %5s | %s"%(row[6],row[7],row[8],row[0],row[1],row[5]))

#Determina si existe un heap expicito en todos los datos
def haveHeapInLines(lines):
    haveHeap=False
    for row in lines:
        if exist(row[5],"heap"): #vemos si coincide la palabra heap
            haveHeap=True
    return haveHeap #si recorrio todos sin que lo encontrara, regresa un false

#el procesamiento de datos se hace en esta funcion
def seccionesMemoria(file):
    #partimos las lineas por los saltos de pagina
    lines=file.split('\n')
    temporal=[]
    #partimos esas lineas por espacios y los metemos en elements
    for i in range (0,lines.__len__()):
        aux=lines[i].split()
        temporal.append(aux)
    
    lines=temporal   
    #sacamos el ultimo elemento y checamos si esta vacio, en caso contrario lo regresamos
    lastLine=lines.pop()
    if lastLine.__len__()>0:
        lastLine.append(lastLine)
    
    #Recorremos todas las lineas y si alguna no tiene su archivo, le ponemos anon
    for i in range(0,lines.__len__()):
        if lines[i].__len__()==5:
            lines[i].append("[anon]")
            
    #Esta parte detecta si no tenemos un heap, y lo determina   
    if haveHeapInLines(lines)==False:
        print("Tu proceso no tiene un heap determinado, voy a encontrarlo, por favor ingresa el numero en DECIMAL")
        TOLERANCIA=int(input("A tu consideracion, el salto en bytes del heap a las bibliotecas  debe ser mayor a :"))
        paseRegionTexto=False
        paseRegionDatos=False
        #iteramos todas las lineas
        for i in range (0,lines.__len__()-1):
            #si la linea es un anonimo, analizaremos si es posible que sea heap
            if exist(lines[i][5],"anon")==True:
                direccionReferencia= retDirB(lines[i]) #obtenemos la direccion de termino del anon
                nextDireccion=retDirA(lines[i+1])#obtenemos la direccion en la que inicia el siguiente
                distancia=int(restaHex(nextDireccion,direccionReferencia),16)#vemos cuanta separacion tienen amabs direcciones
                #Vemos si la distancia es mayor que la TOLERANCIA ingresada, ademas de haber pasado por las regiones data y text
                if distancia>TOLERANCIA and paseRegionDatos==True and paseRegionTexto==True:
                    lines[i].pop()#quitamos el elemento que nos dice que es un [anon]
                    lines[i].append("[heap]")#metemos el elemento que nos dice que es un  heap
                    break #una vez encontrado, vamos a salir del ciclo
            elif exist(lines[i][1],"x")==True: #si no es anonimo, veremos si es ejecutable (texto)      
                paseRegionTexto=True #marcamos que ya pasamos por la region de texto
            elif exist(lines[i][1],"w")==True: #si no es anonimo, veremos si es escribible (data)
                paseRegionDatos=True#marcamos que ya pasamos por la region de datos
            if i>=lines.__len__():
                return []
        
    
    #vamos a determinar la columna uso
    counter=0 #contador para analizar todas las lineas del archivo
    bib="" 
    actualLine=lines[counter]    
    while True:
        permisos=actualLine[1] #obtenemos la cadena de persmisos
        origen=actualLine[5] #obtenemos nombre del archivo asociado, si es anonimo o las otras regiones de memoria
        
        deleted=False
        while actualLine.__len__()>6:
            sobrante=actualLine.pop()
            if exist(sobrante,"deleted")==True:
                deleted=True
            
        if exist(origen,"[")==False: #si no tiene este caracter significa que no es un anon,stack,heap, etc
            if deleted==True:
                actualLine.append("(deleted)")
            elif exist(permisos,"x")==True: # si tiene permisos de ejecucion, es de texto
                actualLine.append(bib+"Texto")
            elif exist(permisos,"w")==True: #si tiene de escritura, es e datos
                actualLine.append(bib+"Datos")
            elif exist(permisos,"r")==True: #si tiene de lectura, es de datos
                actualLine.append(bib+"Datos")
            else:
                actualLine.append("") #si no es de ninguno, lo deja vacio
        else: #si tiene ese caracter "[" vamos a determinar de que region se trata
            if exist(origen,"anon")==True:
                actualLine.append("Anon")
            elif exist(origen,"stack")==True:
                actualLine.append("Stack")
            elif exist(origen,"heap")==True:
                actualLine.append("Heap")
                bib="bib->" #si es el heap, ya nos pasamos de esa region, y los demas Datos y Textos son de bibliotecas
            else:
                actualLine.append("????") #si tiene otro contenido, se pone un desconocido
        
        size=restaHex(retDirB(actualLine),retDirA(actualLine))
        size=int(size,16)
        size=size/1024
        actualLine.append("%d kb"%size)
        numPaginas=size/4
        if size%4!=0:
            numPaginas=numPaginas+1
        actualLine.append("%d pag"%numPaginas)
        counter=counter+1 #aumentamos uno el contaodr
        if counter>=lines.__len__():
            break #si el contador es igual a la cantidad de lineas, se saldrá del while
        else:
            actualLine=lines[counter] #en caso contrario, actualizamos la linea actual
    
    return lines

#funcion que determina las zonas de memoria
def direccionesClave(rows):
    dirIniciaTexto=retDirA(rows[0])
    counter= 0
    pasePorTexto=False
    #primero detectamos la zona de texto
    while True:
        actual=rows[counter]
        if exist(actual[6],"Texto")==True:
            pasePorTexto=True
        #Esta condicion hace que minimo hayamos pasado por un row de texto
        elif exist(actual[6],"Datos")==True and pasePorTexto==True:
            dirTerminaTexto=retDirA(actual)
            break
        #este counter nos hace avanzar por toda la lista
        if counter+1<rows.__len__():
            counter=counter+1
        else:#si avanzamos mas de lo que deberia, nos dice que no pudo y termina la ejecucion
            print("Problema al delimitar la region de texto")
            return []
    dirIniciaDatos=dirTerminaTexto
    #encontraremos hasta donde abarca la region de datos
    while True:
        actual=rows[counter]
        #la seccion de datos acaba cuando encuentra el heap
        if exist(actual[6],"Heap")==True:
            dirTerminaDatos=retDirB(rows[counter-1])
            break
        if counter+1<rows.__len__():
            counter=counter+1
        else:
            print("Problema al delimitar la region de datos")
            return[]
    #guardamos la direccion que acabamos de encontrar del heap
    dirIniciaHeap=retDirA(actual)
    dirTerminaHeap=retDirB(actual)
    #seguimos analizando
    counter=counter+1
    actual=rows[counter]
    dirIniciaBib=retDirA(actual)
    #determinaremos en que direccion acaban las bibliotecas
    while True:
        actual=rows[counter]
        #esta seccion acaaban hasta que el siguiente es el stack
        if exist(rows[counter+1][6],"Stack")==True:
            dirTerminaBib=retDirB(actual)
            counter=counter+1
            actual=rows[counter]
            break
        if counter+1<rows.__len__()-1:
            counter=counter+1
        else:
            print("Problema al delimitar la region de bibliotecas")
            return[]
    #por ultimo ya tenemos el stack, solo guardamos su direccion de inicio A y su direccion de termino B
    dirIniciaStack=retDirA(actual)
    dirTerminaStack=retDirB(actual)
    
    return [dirIniciaTexto,dirTerminaTexto,dirIniciaDatos,dirTerminaDatos,dirIniciaHeap,dirTerminaHeap,dirIniciaBib,dirTerminaBib,dirIniciaStack,dirTerminaStack]    
    
#id=str(7455)
id=str(input("Dame el numero: "))
#abrimos el archivo
f= open('/proc/'+id+'/maps','r')
file= f.read()
titles=[" Direciones "," Perm "," "," "," "," Ubicacion o uso ","Uso","Tam","Pags"]
rows=seccionesMemoria(file)
if rows.__len__()==0:
    print("Ocurrió un error, lo lamento")
    exit()
printFormat(titles)
for row in rows:
    printFormat(row)
values=direccionesClave(rows)

if values.__len__()==0:
    print("No logré determinar las regiones")
else:
    print("Regiones para imagen: ")
    print("Texto: ",values[0],"-",values[1])
    print("Datos: ",values[2],"-",values[3])
    print("Heap: ",values[4],"-",values[5])
    print("Bibliotecas: ",values[6],"-",values[7])
    print("Stack: ",values[8],"-",values[9])
f.close()

