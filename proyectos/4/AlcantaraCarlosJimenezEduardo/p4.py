# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 12:09:32 2020

@author: Charles Alcantara
"""
import os,time,math

def main():
    global f
    global clusterLenght
    global numClustersD
    global numClustersU
    global entradaDirectorioLen
    
    
    f= open("FiUnamFS.img","br+")
    
    nombre=f.read(8)
    if nombre!=b'FiUnamFS':
        printError("El nombre del sistema de archivos no coincide")
        return
    entradaDirectorioLen=64
    version=read(10,13)
    etiquetaVol=read(20,35)
    clusterLenght=int(read(40,45))
    numClustersD=int(read(47,49))
    numClustersU=int(read(52,60))
    
    
    """
    print(directorioToString())
    print("prueba 2")
    agregarArchivo("serieMOSFET.py")
    print(directorioToString())
    
    
    
    print("prueba 3")
    print(byteToString(read(4*1024,33*1024)))
    print("olovorgo------olovorgo")
    print(byteToString(read(34*1024,35*1024)))
    
    
    borrarDelDirectorio("serieMOSFET.py")
    print(read(1024,2048))
    print(byteToString(read(34*1024,35*1024)))
    
    print("prueba 4")
    agregarArchivo("IMG_0395.jpg")
    agregarArchivo("dos.txt")
    agregarArchivo("serieMOSFET.py")
    
    
    print(directorioToString())
    print(read(1024,2048))
    print(read(34*1024,40*1024))
    borrarDelDirectorio("serieMOSFET.py")
    borrarDelDirectorio("IMG_0395.jpg")
    borrarDelDirectorio("dos.txt")
    """
    getArchivo("","datetime.txt")
    
    
    #print(read(1*1024,4*1024))
    #desfragmentar()
    #print("********")
    print(read(5*1024,34*1024))
    
    f.close()
    
def fechaFormato(segundos):
    date=time.gmtime(segundos)
    fechaConFormato=time.strftime("%Y%m%d%H%M%S",date)
    return bytes(fechaConFormato,"utf-8")
    
    
def obtenerDirectorio():
    global clusterLenght
    global numClustersD
    global numClustersU
    global entradaDirectorioLen
    lista=[]
    for i in range(int(clusterLenght),int(clusterLenght)*(int(numClustersD)+1),int(entradaDirectorioLen)):
        lista.append(read(i,i+entradaDirectorioLen))
    return lista
        
def printError(mensajeError):    
    print("Error: "+mensajeError)

def read(a,b):
    global f
    save=f.tell()
    f.seek(a,0)
    b=b-a
    res=f.read(b)
    f.seek(save,0)
    return res        

def byteToString(a):
    return a.decode("utf-8")

def directorioToString():
    directorio=obtenerDirectorio()
    directorioString=""
    for i in range(0,directorio.__len__()):
        actual=byteToString(directorio[i][:15])
        if "Xx.xXx.xXx.xXx."!=actual:
            directorioString=directorioString+actual+"\n"
    return directorioString

def clustersNec(tam):
    global clusterLenght
    clustersNecesarios=tam/clusterLenght
    if tam%clusterLenght!=0:
        clustersNecesarios=clustersNecesarios+1
    return int(math.trunc(clustersNecesarios))

def agregarArchivo(path):
    global f
    global clusterLenght
    global numClustersD
 
    if os.path.isfile(path)==False:
        printError("No existe el archivo origen:"+path)
        return False
    
    
    tamano=os.stat(path).st_size
    name=insertaEspaciosI(os.path.split(path)[-1])
    name=bytes(name,"utf-8")
    if name.__len__()>15:
        printError("Nombre del archivo muy grande, se permiten solo 15 caracteres")
        return False
    size=intToByte(tamano)
    if size.__len__()>8:
        printError("Archivo muy grande")
        return False
    while size.__len__()<8:
        size=b'0'+size
    
    fecMod=fechaFormato(os.path.getmtime(path))
    fecCrea=fechaFormato(os.path.getctime(path))
    clustersNecesarios=clustersNec(tamano)
    
    mapaMemoria=clustersVacios()
    tamReq=clustersNecesarios
    for i in range(0,mapaMemoria.__len__()):
        if mapaMemoria[i]==True:
            tamReq=tamReq-1
        else:
            tamReq=clustersNecesarios
        if tamReq==0:
            clusterInicial=intToByte(i-(clustersNecesarios-1))
            while clusterInicial.__len__()<5:
                clusterInicial=b'0'+clusterInicial
            newFile=open(path,"br")
            content=newFile.read()
            newFile.close()
            f.seek((i-(clustersNecesarios-1))*clusterLenght)
            f.write(content)
            could=nuevoArchivoEnDirectorio(b''+name+separador()+size+separador()+clusterInicial+separador()+fecCrea+
                                     separador()+fecMod+separador()+separador()+separador()+separador())
            if could==False:
                printError("No se pudo insertar el archivo")
                return False
            else:
                return True

def getArchivo(path,name):
    global f
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    
    nombre=bytes(insertaEspaciosI(name),"utf-8")
    tam=0
    for i in range(clusterLenght,numClustersD*clusterLenght,entradaDirectorioLen):
        row=read(i,i+15)
        if nombre==row:
            cluster=int(read(i+25,i+30))
            tam=int(read(i+16,i+24))
            break
    if tam==0:
        printError("No se encontró el archivo "+name)
        return False
        
    content=read(cluster*clusterLenght,cluster*clusterLenght+tam)
    
    if path.__len__()==0:
        newFile=open(name,"wb")
    else:
        newFile=open(path+"/"+name,"w")
    
    newFile.write(content)
    newFile.close
    return True

def clustersVacios():
    global f
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    mapa=[]
    for i in range(0,numClustersU):
        mapa.append(True)
    for i in range(0,numClustersD+1):
        mapa[i]=False
    for i in range(clusterLenght,numClustersD*clusterLenght,entradaDirectorioLen):
        if b'Xx.xXx.xXx.xXx.'==read(i,i+15):
            continue
        clInicial=int(read(i+25,i+30))
        clNec=clustersNec(int(read(i+16,i+24)))
        for j in range(clInicial,clNec+clInicial):
            mapa[j]=False
    return mapa



def intToByte(a):
    return bytes(str(a),"utf-8")    

def nuevoArchivoEnDirectorio(row):
    global f
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    for i in range(clusterLenght,numClustersD*clusterLenght,entradaDirectorioLen):
        actual=read(i,i+15)
        if b'Xx.xXx.xXx.xXx.'==actual:
            f.seek(i)
            f.write(row)
            return True
    printError("No hay espacio en el directorio")
    return False


def borrarDelDirectorio(word):
    global f
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    
    name=insertaEspaciosI(word)
    for i in range(clusterLenght,numClustersD*clusterLenght,entradaDirectorioLen):
        actual=read(i,i+15)
        if name==byteToString(actual):
            f.seek(i)
            f.write(entradaVacia())
            return True
    printError("No pude eliminar el archivo "+word+". No lo pude encontrar")
    return False
            
def entradaVacia():
    res=b'Xx.xXx.xXx.xXx.'+separador()+b'00000000'+separador()
    res=res+b'00000'+separador()+b'00000000000000'+separador()
    res=res+b'00000000000000'+separador()+separador()+separador()+separador()
    return res
    

def separador():
    return b'\x00'
            
def insertaEspaciosI(word):
    while word.__len__()<15:
        word=' '+word
    return word

def desfragmentar():
    global f
    global clusterLenght
    di=obtenerDirectorio()
    for i in range(0,di.__len__()):
        for j in range (0,di.__len__()-i-1):
            if int(di[j][25:30])>int(di[j+1][25:30]):
                aux=di[j]
                di[j]=di[j+1]
                di[j+1]=aux
    
    for i in range (0,di.__len__()):
        
        if di[i][:15]==b'Xx.xXx.xXx.xXx.':
            continue
        mapa=clustersVacios()
        for j in range(int(di[i][25:30])-1,4,-1):
            if mapa[j]==False:
                clusterInit=j+1
                size=int(di[i][16:24])
                info=read(int(di[i][25:30])*clusterLenght,(int(di[i][25:30])*clusterLenght)+size)
                f.seek(clusterInit*clusterLenght)
                f.write(info)
                could=actualizarRegistro(di[i],clusterInit)
                if could==False:
                    printError("No pude desfragmentar")
                    return False
                else:
                    break
    return True
                
                
def actualizarRegistro(row,clusterInicial):
    global f
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    
    clusInit=intToByte(clusterInicial)
    while clusInit.__len__()<5:
        clusInit=b'0'+clusInit
    for i in range(clusterLenght,numClustersD*clusterLenght,entradaDirectorioLen):
        actual=read(i,i+15)
        if row[:15]==actual:
            f.seek(i+25)
            f.write(clusInit)
            return True
    printError("No pude actualizar el directorio")
    return False



main()