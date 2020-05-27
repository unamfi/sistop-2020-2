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
    
    nombreSistema=input("Ingresa el nombre del archivo .img , si no se encuentra en el directorio actual, escribe su ruta: ")
    f= open(nombreSistema,"br+")
    
    print()
    print()
    #Vamos a leer si es un bloque correcto
    nombre=f.read(8)
    if nombre!=b'FiUnamFS':
        printError("El nombre del sistema de archivos no coincide")
        return
    else:
        print("------------------>Sistema de archivos correcto")
        
    #leemos sus caracteristicas
    entradaDirectorioLen=64
    version=read(10,13)
    etiquetaVol=read(20,35)
    clusterLenght=int(read(40,45))
    numClustersD=int(read(47,49))
    numClustersU=int(read(52,60))
    
    #menu
    print("********************************")
    while True:
        print("--->Opciones: 1.Listar archivos 2.Copiar archivo a tu sistema 3.Copiar archivo de tu sistema a FiUnamFS 4.Desfragmentar 5.Mapa de memoria disponible 6.Borrar archivo 0.Salir")
        op=input("Ingresa el numero de la opcion deseada: ")
        could=False
        if op=="0":
            print("Hasta luego")
            break
        elif op=="1":
            print(directorioToString())
        elif op=="2":
            name=input("Ingresa el nombre del archivo que quieres copiar a tu sistema: ")
            path=input("Ingresa la ruta a donde quieres colocarlo: ")
            could=getArchivo(path, name)
            if could==True:
                print("----------------Hecho!------------------")
        elif op=="3":
            path=input("Ingresa el nombre del archivo, junto con su ruta si es necesario :")
            could=agregarArchivo(path)
            if could==True:
                print("----------------Hecho!------------------")
        elif op=="4":
            could=desfragmentar()
            if could==True:
                print("----------------Hecho!------------------")
        elif op=="5":
            l=clustersVacios()
            print("Cluster---Disponible")
            for i in range (0,l.__len__()):
                print(i,"\t--------\t",l[i])
        elif op=="6":
            name=input("Ingresa el nombre del archivo que quieres borrar: ")
            could = borrarDelDirectorio(name)
            if could==True:
                print("----------------Hecho!------------------")
        else:
            print("Opción inválida")
        print("")
        
    
    f.close()
    
#funcion que transforma de segundos, a la fecha con formato en bytes especifico para el proyecto 
def fechaFormato(segundos):
    date=time.gmtime(segundos)
    fechaConFormato=time.strftime("%Y%m%d%H%M%S",date)
    return bytes(fechaConFormato,"utf-8")
    
#Leemos los clusters correspondientes para generar una lista con el directorio    
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
    print("************Error: "+mensajeError)

#funcion que facilita la lectura, deja el apuntador en donde lo encontró
def read(a,b):
    global f
    save=f.tell()
    f.seek(a,0)
    b=b-a
    res=f.read(b)
    f.seek(save,0)
    return res        

#funcion que devuelve una cadena a partir de los bytes
def byteToString(a):
    return a.decode("utf-8")

#lee el directorio y lo convierte  auna cadena de texto plano
def directorioToString():
    directorio=obtenerDirectorio()
    directorioString=""
    for i in range(0,directorio.__len__()):
        actual=byteToString(directorio[i][:15])
        if "Xx.xXx.xXx.xXx."!=actual:
            directorioString=directorioString+actual+"\n"
    return directorioString

#funcion que calcula el numero entero de clusters que se requieren para almacenar el argumento dado en bytes
def clustersNec(tam):
    global clusterLenght
    clustersNecesarios=tam/clusterLenght
    if tam%clusterLenght!=0:
        clustersNecesarios=clustersNecesarios+1
    return int(math.trunc(clustersNecesarios))

#Funcion principal para agregar un archivo desde una ruta hacia el sistema de archivos FIUNAM
def agregarArchivo(path):
    global f
    global clusterLenght
    global numClustersD
    
    #verificamos que el archivo origen existe
    if os.path.isfile(path)==False:
        printError("No existe el archivo origen:"+path)
        return False
    
    #obtenemos sus propiedades
    tamano=os.stat(path).st_size
    name=insertaEspaciosI(os.path.split(path)[-1])
    name=bytes(name,"utf-8")
    
    #Vemos si el nombre es menor al soportado y que no exista un archivo con su mismo nombre
    if name.__len__()>15:
        printError("Nombre del archivo muy grande, se permiten solo 15 caracteres")
        return False
    if seEncuentra(name)==True:
        printError("Ya existe un archivo con ese nombre")
        return False
    size=intToByte(tamano)
    #vemos si el tamaño sobrepasa la capacidad del directorio
    if size.__len__()>8:
        printError("Archivo muy grande")
        return False
    while size.__len__()<8:
        size=b'0'+size
    
    
    fecMod=fechaFormato(os.path.getmtime(path))
    fecCrea=fechaFormato(os.path.getctime(path))
    clustersNecesarios=clustersNec(tamano)
    
    #calculamos el mapa de espacios disponibles
    mapaMemoria=clustersVacios()
    tamReq=clustersNecesarios
    #checamos en todos los espacios si hay cupo suficiente
    for i in range(0,mapaMemoria.__len__()):
        #esto itera para encontrar el espacio ideal, cada que llega a 0, quiere decir que encontro un bloue contiguo de espacio,
        #si se encuentra un false, se reinicia la cuenta
        if mapaMemoria[i]==True:
            tamReq=tamReq-1
        else:
            tamReq=clustersNecesarios
        #despues de encontrar el espacio ideal relaizamos ultimos ajustes para insertar
        if tamReq==0:
            clusterInicial=intToByte(i-(clustersNecesarios-1))
            #damos formato a las variables
            while clusterInicial.__len__()<5:
                clusterInicial=b'0'+clusterInicial
            #abrimos el archivo que queremos, lo leemos todo y lo pegamos en el espacio vacio 
            newFile=open(path,"br")
            content=newFile.read()
            newFile.close()
            #buscamos el espacio vacio
            f.seek((i-(clustersNecesarios-1))*clusterLenght)
            #escribimos en el espacio vacio
            f.write(content)
            #por ultimo, agregamos en el directorio
            could=nuevoArchivoEnDirectorio(b''+name+separador()+size+separador()+clusterInicial+separador()+fecCrea+
                                     separador()+fecMod+separador()+separador()+separador()+separador())
            if could==False:
                printError("No se pudo insertar el archivo")
                return False
            else:
                return True
    printError("No se pudo insertar, no hay un hueco suficientemente grande para que quepa")

#funcion para sacar un archivo del sistema FIUNAM
def getArchivo(path,name):
    global f
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    
    #obtenemos el nombre con formato
    nombre=bytes(insertaEspaciosI(name),"utf-8")
    tam=0
    found=False
    #lo buscamos para obtener sus propiedades
    for i in range(clusterLenght,(int(numClustersD)+1)*clusterLenght,entradaDirectorioLen):
        row=read(i,i+15)
        if nombre==row:
            cluster=int(read(i+25,i+30))
            tam=int(read(i+16,i+24))
            found=True
            break
    #si nunca lo encontré, se lanzara el error
    if found==False:
        printError("No se encontró el archivo "+name)
        return False
    # si lleamos hasta aqui, todo va bien, leemos el contenido del archivo    
    content=read(cluster*clusterLenght,cluster*clusterLenght+tam)
    
    #si no se especifica el path, se crea el archivo en donde se esta ejecutando
    if path.__len__()==0:
        newFile=open(name,"wb")
    else:
        newFile=open(path+"/"+name,"bw")
    
    #escribimos
    newFile.write(content)
    newFile.close
    return True

#funcion que genera el mapa de clusters vacios
def clustersVacios():
    global f
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    mapa=[]
    for i in range(0,numClustersU):
        mapa.append(True)
    #los primeros clusters son para el superbloque y el directorio, siempre se marcaran como ocupados
    for i in range(0,numClustersD+1):
        mapa[i]=False
    #buscamos cada registro del directorio para marcar la region se su archivo como ocupada
    for i in range(clusterLenght,(int(numClustersD)+1)*clusterLenght,entradaDirectorioLen):
        #omitimos los vacios
        if b'Xx.xXx.xXx.xXx.'==read(i,i+15):
            continue
        clInicial=int(read(i+25,i+30))
        clNec=clustersNec(int(read(i+16,i+24)))
        for j in range(clInicial,clNec+clInicial):
            mapa[j]=False
    return mapa


#funcion que transforma un int a un byte
def intToByte(a):
    return bytes(str(a),"utf-8")    

#funcion de ayuda para agregar un archivo al directorio 
def nuevoArchivoEnDirectorio(row):
    global f
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    #vamos a buscar donde puede ser insertado
    for i in range(clusterLenght,(int(numClustersD)+1)*clusterLenght,entradaDirectorioLen):
        actual=read(i,i+15)
        if b'Xx.xXx.xXx.xXx.'==actual:
            #vamos a la ubicacion del registro vacio
            f.seek(i)
            #escribimos
            f.write(row)
            return True
    #si terminamos de recorrer todo, se manda un error
    printError("No hay espacio en el directorio")
    return False

#devuelve true si encuentra alguna coincidencia en el directorio con el nombre puesto en el parametro word
def seEncuentra(word):
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    name=insertaEspaciosI(word)
    for i in range(clusterLenght,(int(numClustersD)+1)*clusterLenght,entradaDirectorioLen):
        actual=read(i,i+15)
        if name==actual:
            return True
    return False

#se utiliza para borrar del directorio
def borrarDelDirectorio(word):
    global f
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    #nos aseguramos que la palbara esté con buen formato
    name=insertaEspaciosI(word)
    for i in range(clusterLenght,(int(numClustersD)+1)*clusterLenght,entradaDirectorioLen):
        #obtenemos el nombre
        actual=read(i,i+15)
        if name==byteToString(actual):
            #si coincide vamos a el
            f.seek(i)
            #escribimos un registro vacio
            f.write(entradaVacia())
            return True
    #si recorrimos todo, vamos a lanzar error 
    printError("No pude eliminar el archivo "+word+". No lo pude encontrar")
    return False

#funcion que devuelve una entrada vacia            
def entradaVacia():
    res=b'Xx.xXx.xXx.xXx.'+separador()+b'00000000'+separador()
    res=res+b'00000'+separador()+b'00000000000000'+separador()
    res=res+b'00000000000000'+separador()+separador()+separador()+separador()
    return res
    
#funcion que devuelve el separador de atributos 
def separador():
    return b'\x00'

#damos formato a los nombres para que todos sean de long 15            
def insertaEspaciosI(word):
    while word.__len__()<15:
        word=' '+word
    return word

#funcion principal para lograr desfragmentar
def desfragmentar():
    global f
    global clusterLenght
    di=obtenerDirectorio()
    #obtenemos el directorio y ordenamos con base en su "primer cluster"
    #algoritmo bubble sort
    for i in range(0,di.__len__()):
        for j in range (0,di.__len__()-i-1):
            if int(di[j][25:30])>int(di[j+1][25:30]):
                aux=di[j]
                di[j]=di[j+1]
                di[j+1]=aux
    
    #para cada registro consultamos sus datos, vamos a checar si hay clusters vacios antes de ellos 
    for i in range (0,di.__len__()):
        #omitimos los vacios
        if di[i][:15]==b'Xx.xXx.xXx.xXx.':
            continue
        #generamos el mapa de vacios
        mapa=clustersVacios()
        #dir[i][25:30] es el cluster donde se ubica, y se va a detener en el primer cluster para datos
        for j in range(int(di[i][25:30])-1,4,-1):
            #vamos hasta el cluster que no este vacio, a partir de ahi, copiaremos la iformación
            if mapa[j]==False:
                #como tenemos el cluster que si tiene datos, guardamos el siguiente
                clusterInit=j+1
                size=int(di[i][16:24])
                info=read(int(di[i][25:30])*clusterLenght,(int(di[i][25:30])*clusterLenght)+size)
                #vamos al nuevo cluster
                f.seek(clusterInit*clusterLenght)
                #escribimos
                f.write(info)
                #actualizamos registro
                could=actualizarRegistro(di[i],clusterInit)
                #si no pudimos actualizar el regitro, hay un error y salimos del proceso
                if could==False:
                    printError("No pude desfragmentar")
                    return False
                else:
                    break
    return True
                
#nos sirve para actualizar el cluster inicial de un registro a partir de su nombre en row               
def actualizarRegistro(row,clusterInicial):
    global f
    global clusterLenght
    global numClustersD
    global entradaDirectorioLen
    
    clusInit=intToByte(clusterInicial)
    while clusInit.__len__()<5:
        clusInit=b'0'+clusInit
    for i in range(clusterLenght,(int(numClustersD)+1)*clusterLenght,entradaDirectorioLen):
        actual=read(i,i+15)
        if row[:15]==actual:
            f.seek(i+25)
            f.write(clusInit)
            return True
    printError("No pude actualizar el directorio")
    return False



main()