import mmap
import os
import os.path, time
import math
# La superficie del disco se divide en sectores de 256 bytes.
# Cada cluster mide cuatro sectores.
#
#



class BloquePrincipal:
    #El primer cluster (#0) del pseudodispositivo es el superbloque. 
    # Este contiene información en los siguientes bytes
    # chech de aquí saque el uso de mmap.mmap ;v https://rico-schmidt.name/pymotw-3/mmap/
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


    #para mostrar el directorio usaremos         ls
    #para eliminar un archivo usaremos           rm [FILE]
    #para copiar un archivo a nuestro sistema    cpout [FILE]
    #para copiar un archivo al sistema           cpin [FILE]
    #para desfragmentar                          defrag


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

    def buscar (self,archivo):
        for x in range(0,64):
            p = self.bp.tamanio_cluster + i * self.bp.tamanio_entrada
            j = Entrada(self.fs_map[p:p + self.bp.tamanio_entrada])
            if archivo == j.nombreF:
                j.numdir = x
                return j
        return None
    
    def registrar(self,archivo,cluster):
        for x in range(0,64):
            p = self.bp.tamanio_cluster + x*self.bp.tamanio_entrada
            i = Entrada(self.fs_map[p:p + self.bp.tamanio_entrada])
            if self.entrada_no_usada == i.fname:
                #espacios = i.nombre_f - len(archivo)
                #El rjust()método alineará a la derecha la cadena, utilizando un carácter especificado 
                #(el espacio es el predeterminado) como el carácter de relleno.
                # len(archivo)+espacios  => i.nombre_f                                                                         
                self.fs_map[p:p + i.nombre_f] = bytes(archivo.rjust(i.nombre_f),'utf-8')

                #st_size : representa el tamaño del archivo en bytes.
                archivo_tamanio = str(os.stat(archivo).st_size)
                #tam = i.tamanio_f - len(archivo_tamanio)
                nuevo_p = p + i.nombre_f + 1
                #Rellene la cadena con ceros hasta que tenga i.tamanio_f caracteres de longitud:
                self.fs_map[nuevo_p :nuevo_p + i.tamanio_f] = bytes(archivo_tamanio.zfill(i.tamanio_f),'utf-8')

                cluster_archivo = str(cluster)
                #cluster_z = i.cluster_f - len(cluster_archivo)
                nuevo_p += i.tamanio_f + 1
                self.fs_map[nuevo_p:nuevo_p + i.cluster_f] = bytes(cluster_archivo.zfill(i.cluster_f),'utf-8')

                fecha_creacion= time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getctime(archivo)))
                nuevo_p += i.cluster_f + 1
                self.fs_map[nuevo_p:nuevo_p + i.creacion_f] = bytes(fecha_creacion,'utf-8')

                fecha_modif=time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(archivo)))
                nuevo_p += i.creacion_f + 1
                self.fs_map[nuevo_p:nuevo_p + i.modif_f] = bytes(fecha_modif,'utf-8')

                break

    def cpint(self,inodo,cluster_destino):
        p = self.bp.tamanio_cluster * inodo.clusterF
        buffer = self.fs_map[p:p + inodo.tamanioF]
        p_dest=self.bp.tamanio_cluster * cluster_destino
        self.fs_map[p_dest:p_dest + inodo.tamanioF ] = buffer

    def ls(self):
        print("{:10}{:10}{:10}{:10}{:10}{:10}{:10}".format("Nombre","Cluster","Tamaño","Mes","Dia","Año","Hora"))
        for i in self.inodo():
            fecha = FormatoFecha(i.modifF)
            print("{:10}{:10}{:10}{:24}".format(i.nombreF, i.clusterF, i.tamanioF, fecha))

    def FormatoFecha(self,fecha):
        meses={'01':'Ene','02':'Feb','03':'Mar','04':'Abr','05':'May',
            '06':'Jun','07':'Jul','08':'Ago','09':'Sept','10':'Oct','11':'Nov','12':'Dis'}
        a=fecha[0:4]
        m=meses.get(fecha[4:6])
        d=fecha[6:8]
        hh=fecha[8:10]
        mm=fecha[10:12]
        ss=fecha[12:14]
        return "{:6}{:6}{:6}{:6}".format(m,d,a,hh+':'+mm+':'+ss)

    def rm(self,archivo):
        i = self.search(archivo)
        if i is None :
            print("rm: " + archivo + " : Archivo no encontrado ")
        else :
            p = self.bp.tamanio_cluster + self.bp.tamanio_entrada *i.numdir
            self.fs_map[p:p + i.nombre_f] = bytes(self.entrada_no_usada,'utf-8')
    
    def cpout(self,archivo,dir):
        #Primero buscar si el archivo existe,
        #si existe, lo copiamos al directorio especificado
        i = self.buscar(archivo)
        if i is None :
            print("cpout: " + archivo + " : Archivo no encontrado ")
        else :
            p = self.bp.tamanio_cluster + self.bp.tamanio_entrada * i.numdir
            # VERIFICAR QUE EXISTA EL ARCHIVO
            archivocp = open(archivo,"a+b")
            cluster = self.sb.tamanio_cluster * i.clusterF
            archivocp.write(self.fs_map[cluster:cluster + i.tamanioF])
            archivocp.close()

    def cpin(self, archivo):
        if os.path.isfile(archivo):
            if len(archivo) < 15:
                if self.buscar(archivo) != None:
                    print("se encontro un archivo con el mismo nombre, por favor repita la operacíon con un nombre diferente") 
                else:
                    self.Copiar(archivo)
            else:
                print("cpin: " + archivo + ": nombre de archivo demasiado grande, por favor repita la operación con un nombre más corto")
        else:
            print("cpin: " + archivo + " Archivo no encontrado")



            
