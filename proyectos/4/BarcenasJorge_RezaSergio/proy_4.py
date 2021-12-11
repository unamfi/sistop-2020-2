"""
	Proyecto 4: (micro) sistema de archivos
	Profesor: Gunnar Wolf

	Alumnos:
		Barcenas Avelar, Jorge Octavio
		Reza Chavarria, Sergio Gabriel

"""
import mmap
import os
import sys
import os.path, time
import math
"""
 La superficie del disco se divide en sectores de 256 bytes.
 Cada cluster mide cuatro sectores.


	Comandos del programa
    para mostrar el directorio usaremos         ls
    para eliminar un archivo usaremos           rm [FILE]
    para copiar un archivo a nuestro sistema    cpout [FILE]
    para copiar un archivo al sistema           cpin [FILE]
    para desfragmentar                          defrag
"""
class BloquePrincipal:
    #El primer cluster (#0) del pseudodispositivo es el superbloque. 
    # Este contiene información en los siguientes bytes
    f = open('fiunamfs.img','r+b')
    fs_map = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)

    nombre             = fs_map[0:8].decode('utf-8')         # FiUnamFS
    version            = fs_map[10:13].decode('utf-8')       # 0.9
    etiqueta_volumen   = fs_map[20:35].decode('utf-8')       # Nuestro Sistema
    tamanio_cluster    = int(fs_map[40:45].decode('utf-8'))  # 1024   ya que cada cluster tiene 4 sectores 256(4)= 1024
    num_cluster        = int(fs_map[47:49].decode('utf-8'))  # 4      ya que "El directorio está ubicado en los clusters 1 a 4"
    total_clusters     = int(fs_map[52:60].decode('utf-8'))  # 1440 = (1474560/1024) 
    tamanio_entrada    = 64                                  # cada ntrada mide 64 bytes

    #print(total)
    f.close()
    fs_map.close()


#Clase para la obtención de información de las secciones del sistema que se requieren

class Entrada:
    nombre_f    = 15
    tamanio_f   = 8
    cluster_f   = 5
    creacion_f  = 14
    modif_f     = 14

    nombreF = ""         # 0-15
    tamanioF = 0          # 16-24
    clusterF = 0  # 25-30
    creacionF = ""      # 31-45
    modifF = ""        # 46-60
    numdir = -1        # numero entre 0-63

    def __init__(self, entrada):
        self.nombreF   = entrada[0:15].decode('utf-8').lstrip()
        self.tamanioF  = int(entrada[16:24].decode('utf-8'))
        self.clusterF  = int(entrada[25:30].decode('utf-8'))
        self.creacionF = entrada[31:45].decode('utf-8')
        self.modifF    = entrada[46:60].decode('utf-8')

#Clase principal que utilizará el micro sistema, junto con las operaciones de este.
class SistArch:
    f = open('fiunamfs.img','a+b')
    fs_map = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_WRITE)
    bp = BloquePrincipal()
    entrada_no_usada ='Xx.xXx.xXx.xXx.'

    def inodo(self):
        inodos = []
        
        for i in range(0,64):
            #simularemos un cabezal que señale donde inician los metadatos
            #el cluster 0 es el bloque principal
            #debemos recorrernos hasta el bloque 1
            # cada cluster mide 1024 * 4 = 4096 tamaño de los 4 clusters donde se aloja el direcotorio
            # con entradas de 64 
            #64 * 64 = 4096
            #64 * 63 = 4032 (63 porque sera el ultimo lugar donde podra entra una entrada)
            # 1024 + ( [0,63] * 64 )  
            p = self.bp.tamanio_cluster + i * self.bp.tamanio_entrada
            j = Entrada(self.fs_map[p:p + self.bp.tamanio_entrada])
            if self.entrada_no_usada != j.nombreF:
                j.numdir = i
                inodos.append(j)
        return inodos
    #Método de busqueda
    def buscar (self,archivo):
        for x in range(0,64):
            p = self.bp.tamanio_cluster + x * self.bp.tamanio_entrada
            j = Entrada(self.fs_map[p:p + self.bp.tamanio_entrada])
            if archivo == j.nombreF:
                j.numdir = x
                return j
        return None
    #Método de registro de archivo
    def registrar(self,archivo,cluster):
        for x in range(0,64):
            p = self.bp.tamanio_cluster + x*self.bp.tamanio_entrada
            i = Entrada(self.fs_map[p:p + self.bp.tamanio_entrada])
            if self.entrada_no_usada == i.nombreF:
                #espacios = i.nombre_f - len(archivo)
                #El rjust()método alineará a la derecha la cadena, utilizando un carácter especificado 
                #(el espacio es el predeterminado) como el carácter de relleno.
                # len(archivo)+espacios  => i.nombre_f                                                                         
                self.fs_map[p:p + i.nombre_f] = archivo.rjust(i.nombre_f).encode('utf-8')

                #st_size : representa el tamaño del archivo en bytes.
                archivo_tamanio = str(os.stat(archivo).st_size)
                #tam = i.tamanio_f - len(archivo_tamanio)
                nuevo_p = p + i.nombre_f + 1
                #Rellene la cadena con ceros hasta que tenga i.tamanio_f caracteres de longitud:
                self.fs_map[nuevo_p :nuevo_p + i.tamanio_f] = archivo_tamanio.zfill(i.tamanio_f).encode('utf-8')

                cluster_archivo = str(cluster)
                #cluster_z = i.cluster_f - len(cluster_archivo)
                nuevo_p += i.tamanio_f + 1
                self.fs_map[nuevo_p:nuevo_p + i.cluster_f] = cluster_archivo.zfill(i.cluster_f).encode('utf-8')

                fecha_creacion= time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getctime(archivo)))
                nuevo_p += i.cluster_f + 1
                self.fs_map[nuevo_p:nuevo_p + i.creacion_f] = fecha_creacion.encode('utf-8')

                fecha_modif=time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(archivo)))
                nuevo_p += i.creacion_f + 1
                self.fs_map[nuevo_p:nuevo_p + i.modif_f] = fecha_modif.encode('utf-8')

                break


    #Método de obtención de información
    def ls(self):
        print("{:15}{:15}{:10}{:32}{:30}".format("Nombre","Cluster","Tamaño","Fecha y hora de Modificación","Fecha y hora de creación"))
        for i in self.inodo():
        	fecha_c= self.FormatoFecha(i.creacionF)
        	fecha_m = self.FormatoFecha(i.modifF)
        	print("{:15}{:8}{:12}{:24}{:24}".format(i.nombreF, i.clusterF, i.tamanioF, fecha_c,fecha_m))
    
   	#Método para eliminación de información
    def rm(self,archivo):
        i = self.buscar(archivo)
        if i is None :
            print(archivo + " : Archivo no encontrado ")
        else :
            p = self.bp.tamanio_cluster + self.bp.tamanio_entrada *i.numdir
            self.fs_map[p:p + i.nombre_f] = bytes(self.entrada_no_usada,'utf-8')
            self.fs_map[p+16:p+24]=bytes("".zfill(8),'utf-8')
            self.fs_map[p+25:p+30]=bytes("".zfill(5),'utf-8')
            self.fs_map[p+31:p+45]=bytes("".zfill(14),'utf-8')
            self.fs_map[p+46:p+60]=bytes("".zfill(14),'utf-8')

    #Método para copiar en nuestro sistema
    def cpout(self,archivo,dir):
        #Primero buscar si el archivo existe,
        #si existe, lo copiamos al directorio especificado
        i = self.buscar(archivo)
        if i is not None :
            if os.path.exists(dir):
                p = self.bp.tamanio_cluster + self.bp.tamanio_entrada * i.numdir
                archivocp = open(dir+"/"+archivo,"a+b")
                cluster = self.bp.tamanio_cluster * i.clusterF
                archivocp.write(self.fs_map[cluster:cluster + i.tamanioF])
                archivocp.close()
            else:
                print("Dirección " + dir+" no encontrada")
        else:
            print(i.nombreF + " : Archivo no encontrado ")
    #Método para comprobar si es posible copiar al sistema FiUnamFS
    def cpin(self, archivo):
        if os.path.isfile(archivo):
            if len(archivo) < 15:
                if self.buscar(archivo) != None:
                    print("se encontro un archivo con el mismo nombre, por favor repita la operacíon con un nombre diferente") 
                else:
                    self.Copiar(archivo)
            else:
                print(archivo + ": nombre de archivo demasiado grande, por favor repita la operación con un nombre más corto")
        else:
            print(archivo + " Archivo no encontrado")

    #Metodo de copiado de archivos hacia el sistema FiUnamFS
    def Copiar(self, archivo):
        inodos = self.inodo()
        inodos.sort(key = lambda x : x.clusterF)
        tam_archivo = os.stat(archivo).st_size
        #El método de número de Python ceil () devuelve el valor máximo de x :
        #  el entero más pequeño, no menor que x.
        cluster_archivo = math.ceil(tam_archivo/self.bp.tamanio_cluster)

        #si no hay archivos el primero lo meteremos en el cluster 5 
        if len(inodos) == 0:
            #los clusters que ocupa el archivo debe ser menor al espacio disponible
            if  cluster_archivo <= (self.bp.total_clusters - 4):
                f = open(archivo,"rb")
                #lo meteremos en el cluster 5
                destino = self.bp.tamanio_cluster * 5
                self.fs_map[destino: destino + tam_archivo] = f.read()
                self.registrar(archivo,5)
                f.close()
            else:
                print(archivo + " demasiado grande")
        else:
            copiado = False
            for j in range(0,len(inodos)-1):
                #                 cluster           +           (tamaño del archivo / 1024)
                ultimo_cluster = inodos[j].clusterF + math.ceil( inodos[j].tamanioF / self.bp.tamanio_cluster)
                espacio_entre_sig_archivo = inodos[j+1].clusterF - ultimo_cluster

                if cluster_archivo <= espacio_entre_sig_archivo:
                    f = open(archivo, "rb")
                    p = int(self.bp.tamanio_cluster * (cluster_archivo + 1))
                    self.fs_map[p : p + tam_archivo ] = f.read()
                    self.registrar(archivo,cluster_archivo + 1)
                    f.close()
                    copiado = True
                    break
            # si no hubo espacio entre archivos lo intentaremos copiar al final
            if copiado == False:
                #            cluster del ultimo archivo
                ultimo = inodos[len(inodos) - 1].clusterF + math.ceil(inodos[len(inodos) - 1].tamanioF / self.bp.tamanio_cluster )
                espacio_restante = self.bp.total_clusters - ultimo
                if cluster_archivo <= espacio_restante:
                    f = open(archivo,"rb")
                    p = self.bp.total_clusters * (ultimo + 1)
                    self.fs_map[p : p + tam_archivo] = f.read()
                    self.registrar(archivo, ultimo + 1)
                    f.close()
                    copiado = True
                else:
                    print(archivo + "Archivo demasido grande")
    #Método para desfragmentar 
    def defrag(self):
    	for i in range(0,64): 
            p = self.bp.tamanio_cluster + i * self.bp.tamanio_entrada
            j = Entrada(self.fs_map[p:p + self.bp.tamanio_entrada])
            #print("{} + {} + {}".format(i,j.nombreF,j.clusterF))
            if (j.nombreF==self.entrada_no_usada):
            	for k in range (i+1,64):
            		paux = self.bp.tamanio_cluster + k * self.bp.tamanio_entrada
            		jaux = Entrada(self.fs_map[paux:paux + self.bp.tamanio_entrada])
            		if(jaux.nombreF!=self.entrada_no_usada):
            			self.fs_map[p:p + self.bp.tamanio_entrada]=self.fs_map[paux:paux + self.bp.tamanio_entrada]
            			self.fs_map[paux:paux + 15]=bytes(self.entrada_no_usada,'utf-8')
            			self.fs_map[paux+16:paux+24]=bytes("".zfill(8),'utf-8')
            			self.fs_map[paux+25:paux+30]=bytes("".zfill(5),'utf-8')
            			self.fs_map[paux+31:paux+45]=bytes("".zfill(14),'utf-8')
            			self.fs_map[paux+46:paux+60]=bytes("".zfill(14),'utf-8')
            			break
    	print("Defrag Complete")
    #Método de prueba para checar si se realizó la desfragmentación
    def printall (self):
        print("entrada + archivo + cluster + fecha_modificación   \t\t + fecha_creación")
        for i in range (0,64):
            p = self.bp.tamanio_cluster + i * self.bp.tamanio_entrada
            j = Entrada(self.fs_map[p:p + self.bp.tamanio_entrada])
            if j.nombreF == self.entrada_no_usada:
                print("{:2} + {:15} + {:4} + {:30} + {:20}".format(i,j.nombreF,j.clusterF,j.creacionF,j.modifF))
            else:
                print("{:2} + {:15} + {:4} + {:29} + {:20}".format(i,j.nombreF,j.clusterF,self.FormatoFecha(j.creacionF),self.FormatoFecha(j.modifF)))
    #Método para la impresión de la fecha
    def FormatoFecha(self,fecha):
        meses={'01':'Ene','02':'Feb','03':'Mar','04':'Abr','05':'May',
            '06':'Jun','07':'Jul','08':'Ago','09':'Sept','10':'Oct','11':'Nov','12':'Dis'}
        a=fecha[0:4]
        m=meses.get(fecha[4:6])
        d=fecha[6:8]
        hh=fecha[8:10]
        mm=fecha[10:12]
        ss=fecha[12:14]
        return "{:8}{:5}{:6}{:10}".format("\t"+m,d,a,hh+':'+mm+':'+ss)
    def message(self):        
        print("ls                   ->        Mostrar directorio")
        print("printall             ->        Mostrar los 64 espacios para entradas")
        print("rm    [FILE]         ->        Eliminar Archivo")
        print("cpout [FILE] \"DIR\"   ->        Copiar archivo a nuestro sistema")
        print("cpin  [FILE]         ->        Copiar archivo al sistema")
        print("defrag               ->        Desfragmentación")    

def main():
    sistema = SistArch()
    if(len(sys.argv)==2):
        if(sys.argv[1]=='ls'):
            sistema.ls()
        elif(sys.argv[1]=='printall'):
            sistema.printall()
        elif(sys.argv[1]=='printall'):
            sistema.printall()
        elif(sys.argv[1]=='defrag'):
            sistema.defrag()
        elif(sys.argv[1]=='-help'):
            sistema.message()
        else:
            print("Comando no encontrado. Escriba -help para revisar lista de comandos")
    elif(len(sys.argv)==3):
        if(sys.argv[1]=='cpin'):
            sistema.cpin(sys.argv[2])
        elif(sys.argv[1]=='rm'):
            sistema.rm(sys.argv[2])
        else:
            print("Comando no encontrado. Escriba -help para revisar lista de comandos")
    elif(len(sys.argv)==4):
        if(sys.argv[1]=='cpout'):
            sistema.cpout(sys.argv[2],sys.argv[3])
        else:
            print("Comando no encontrado. Escriba -help para revisar lista de comandos")
    else:
        print("Comando no encontrado. Escriba -help para revisar lista de comandos")
if __name__ == '__main__':
    main()






