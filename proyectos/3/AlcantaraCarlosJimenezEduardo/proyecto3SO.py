# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math

def restaHex(a,b):
    numA=int(a,16)
    numB=int(b,16)
    return hex(numA-numB)

def retDirA(row):
    d=row[0].split('-')
    return d[0]

def retDirB(row):
    d=row[0].split('-')
    return d[1]

def exist(word,character):
    compare=word.find(character)
    if compare!=-1:
        return True
    else:
        return False

def printFormat(row):
    print("|%10s | %25s | %5s | %10s | %5s | %10s | %s"%(row[6],row[0],row[1],row[2],row[3],row[4],row[5]))

def haveHeapInLines(lines):
    haveHeap=False
    for row in lines:
        if exist(row[5],"heap"):
            haveHeap=True
    return haveHeap

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
    
    
    for i in range(0,lines.__len__()):
        if lines[i].__len__()==5:
            lines[i].append("[anon]")
    
    global TOLERANCIA    
    if haveHeapInLines(lines)==False:
        print("Tu proceso no tiene un heap determinado, voy a calcularlo, por favor ingresa el numero en HEXADECIMAL")
        TOLERANCIA=int(input("A tu consideracion, el salto en bytes del heap a las bibliotecas  debe ser mayor a :"))
        for i in range (0,lines.__len__()-1):
            if exist(lines[i][5],"anon")==True:
                direccionReferencia= retDirB(lines[i])
                nextDireccion=retDirA(lines[i+1])
                distancia=int(restaHex(nextDireccion,direccionReferencia),16)
                print("D",distancia,"TOL",TOLERANCIA,"i ",i) 
                if distancia>TOLERANCIA:
                    lines[i].pop()
                    lines[i].append("[heap]")
                    break
                
            
          
    
    counter=0 #contador para analizar todas las lineas del archivo
    bib=""
    actualLine=lines[counter]    
    while True:
        permisos=actualLine[1]
        origen=actualLine[5]
        if exist(origen,"[")==False:
            if exist(permisos,"x")==True:
                actualLine.append(bib+"Texto")
            elif exist(permisos,"w")==True:
                actualLine.append(bib+"Datos")
            elif exist(permisos,"r")==True:
                actualLine.append(bib+"Datos")
            else:
                actualLine.append("")
        else:
            if exist(origen,"anon")==True:
                actualLine.append("anon")
            elif exist(origen,"stack")==True:
                actualLine.append("stack")
            elif exist(origen,"heap")==True:
                actualLine.append("heap")
                bib="bib->"
            else:
                actualLine.append("????")
        counter=counter+1
        if counter>=lines.__len__():
            break
        else:
            actualLine=lines[counter]
        
    for line in lines:
        printFormat(line)
     
TOLERANCIA=str(400)        
id=str(3333)
#id=str(input("Dame el numero: "))
f= open('/proc/'+id+'/maps','r')
file= f.read()
print(file)
seccionesMemoria(file)
f.close()

