import mmap
import os
import sys
import os.path, time
import math
import re

class SuperBloque:
    try:
        f = open('fiunamfs.img','r+b')
        imagen = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
        nombre             = imagen[0:8].decode('utf-8')      
        version            = imagen[10:13].decode('utf-8')
        etiqueta_volumen   = imagen[20:35].decode('utf-8')
        tamanio_cluster    = int(imagen[40:45].decode('utf-8'))
        num_cluster        = int(imagen[47:49].decode('utf-8'))
        total_clusters     = int(imagen[52:60].decode('utf-8'))
        tamanio_entrada    = 64                               
        f.close()
        imagen.close()
    except IOError:
        print("Error al abrir el sistema de archivos ")

class Entrada:
    nombre_archivo = 15
    tamanio_archivo = 8
    num_cluster = 5
    fechaCreacion = 14
    fecha_modificacion = 14

    def __init__(self, entrada):
        self.nombreArchivo   = entrada[0:15].decode('utf-8').lstrip()
        self.tamanoArchivo   = int(entrada[16:24].decode('utf-8'))
        self.NumClusters     = int(entrada[25:30].decode('utf-8'))
        self.fecha_crea      = entrada[31:45].decode('utf-8')
        self.fecha_modif     = entrada[46:60].decode('utf-8')


class SistemaArchivosSGJC:
    f = open('fiunamfs.img','a+b')
    imagen = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_WRITE)
    SuperBloque = SuperBloque()
    sinUsar ='Xx.xXx.xXx.xXx.'

    def inodo(self):
        inodos = []
        for i in range(64):
            p = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada
            j = Entrada(self.imagen[p:p + self.SuperBloque.tamanio_entrada])
            if self.sinUsar != j.nombreArchivo:
                j.numdir = i
                inodos.append(j)
        return inodos

    def buscar (self,archivo):
        for x in range(64):
            p = self.SuperBloque.tamanio_cluster + x * self.SuperBloque.tamanio_entrada
            j = Entrada(self.imagen[p:p + self.SuperBloque.tamanio_entrada])
            if archivo == j.nombreArchivo:
                j.numdir = x
                return j

    def registrar(self,archivo,cluster):
        for x in range(64):
            p = self.SuperBloque.tamanio_cluster + x*self.SuperBloque.tamanio_entrada
            i = Entrada(self.imagen[p:p + self.SuperBloque.tamanio_entrada])
            if self.sinUsar == i.nombreArchivo:
                                                                                       
                self.imagen[p:p + i.nombre_archivo] = archivo.rjust(i.nombre_archivo).encode('utf-8')
                archivo_tamanio = str(os.stat(archivo).st_size)
                nuevo_p = p + i.nombre_archivo + 1
                self.imagen[nuevo_p :nuevo_p + i.tamanio_archivo] = archivo_tamanio.zfill(i.tamanio_archivo).encode('utf-8')

                cluster_archivo = str(cluster)
              
                nuevo_p += i.tamanio_archivo + 1
                self.imagen[nuevo_p:nuevo_p + i.num_cluster] = cluster_archivo.zfill(i.num_cluster).encode('utf-8')

                fecha_creacion= time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getctime(archivo)))
                nuevo_p += i.num_cluster + 1
                self.imagen[nuevo_p:nuevo_p + i.fechaCreacion] = fecha_creacion.encode('utf-8')

                fecha_modif=time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(archivo)))
                nuevo_p += i.fechaCreacion + 1
                self.imagen[nuevo_p:nuevo_p + i.fecha_modificacion] = fecha_modif.encode('utf-8')

                break

    def ls(self):
        
        print("{:15}{:15}{:10}{:32}{:30}".format("Nombre","Cluster","Tamaño","Fecha y hora de Modificación","Fecha y hora de creación"))
        for i in self.inodo():
            tamanioArchivo = convertir(i.tamanoArchivo)
            fecha_c= self.ObtenerFecha(i.fecha_crea)
            fecha_m = self.ObtenerFecha(i.fecha_modif)
            print(i.nombreArchivo, i.NumClusters, tamanioArchivo, fecha_c,fecha_m)
    
    def eliminar(self,archivo):
        i = self.buscar(archivo)
        if i is None :
            print(archivo + " : Archivo no encontrado ")
        else :
            p = self.SuperBloque.tamanio_cluster + self.SuperBloque.tamanio_entrada *i.numdir
            self.imagen[p:p + i.nombre_archivo] = bytes(self.sinUsar,'utf-8')
            self.imagen[p+16:p+24]=bytes("".zfill(8),'utf-8')
            self.imagen[p+25:p+30]=bytes("".zfill(5),'utf-8')
            self.imagen[p+31:p+45]=bytes("".zfill(14),'utf-8')
            self.imagen[p+46:p+60]=bytes("".zfill(14),'utf-8')

    #Método para copiar en nuestro sistema
    def cpout(self,archivo,dir):
        #Primero buscar si el archivo existe,
        #si existe, lo copiamos al directorio especificado
        i = self.buscar(archivo)
        if i is not None :
            if os.path.exists(dir):
                p = self.SuperBloque.tamanio_cluster + self.SuperBloque.tamanio_entrada * i.numdir
                archivocp = open(dir+"/"+archivo,"a+b")
                cluster = self.SuperBloque.tamanio_cluster * i.NumClusters
                archivocp.write(self.imagen[cluster:cluster + i.tamanoArchivo])
                archivocp.close()
            else:
                print("Dirección " + dir+" no encontrada")
        else:
            print(i.nombreArchivo + " : Archivo no encontrado ")
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
        inodos.sort(key = lambda x : x.NumClusters)
        tam_archivo = os.stat(archivo).st_size
        #El método de número de Python ceil () devuelve el valor máximo de x :
        #  el entero más pequeño, no menor que x.
        cluster_archivo = math.ceil(tam_archivo/self.SuperBloque.tamanio_cluster)

        #si no hay archivos el primero lo meteremos en el cluster 5 
        
                    break
            # si no hubo espacio entre archivos lo intentaremos copiar al final
            if copiado == False:
                #            cluster del ultimo archivo
                ultimo = inodos[len(inodos) - 1].NumClusters + math.ceil(inodos[len(inodos) - 1].tamanoArchivo / self.SuperBloque.tamanio_cluster )
                espacio_restante = self.SuperBloque.total_clusters - ultimo
                if cluster_archivo <= espacio_restante:
                    f = open(archivo,"rb")
                    p = self.SuperBloque.total_clusters * (ultimo + 1)
                    self.imagen[p : p + tam_archivo] = f.read()
                    self.registrar(archivo, ultimo + 1)
                    f.close()
                    copiado = True
                else:
                    print(archivo + "Archivo demasido grande")
    #Método para desfragmentar 
    def defrag(self):
        for i in range(64): 
            p = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada
            j = Entrada(self.imagen[p:p + self.SuperBloque.tamanio_entrada])
            #print("{} + {} + {}".format(i,j.nombreArchivo,j.NumClusters))
            if (j.nombreArchivo==self.sinUsar):
                for k in range (i+1,64):
                    paux = self.SuperBloque.tamanio_cluster + k * self.SuperBloque.tamanio_entrada
                    jaux = Entrada(self.imagen[paux:paux + self.SuperBloque.tamanio_entrada])
                    if(jaux.nombreArchivo!=self.sinUsar):
                        self.imagen[p:p + self.SuperBloque.tamanio_entrada]=self.imagen[paux:paux + self.SuperBloque.tamanio_entrada]
                        self.imagen[paux:paux + 15]=bytes(self.sinUsar,'utf-8')
                        self.imagen[paux+16:paux+24]=bytes("".zfill(8),'utf-8')
                        self.imagen[paux+25:paux+30]=bytes("".zfill(5),'utf-8')
                        self.imagen[paux+31:paux+45]=bytes("".zfill(14),'utf-8')
                        self.imagen[paux+46:paux+60]=bytes("".zfill(14),'utf-8')
                        break
        sys.stdout.write('\n\t'+'\x1b[1;32m' + 'Desfragmentación completa! :) ' + '\x1b[0m'+'\n\n')
    #Método de prueba para checar si se realizó la desfragmentación
    def mostrarTodo (self):
        print("IN  Nombre archivo   cluster  Fecha de creación      \t      Fecha de modificación")
        for i in range (64):
            p = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada
            j = Entrada(self.imagen[p:p + self.SuperBloque.tamanio_entrada])
            if j.nombreArchivo == self.sinUsar:
                print("{:2}  {:15}     {:4}  {:30}  {:20}".format(i,j.nombreArchivo,j.NumClusters,j.fecha_crea,j.fecha_modif))
            else:
                print("{:2}  {:15}     {:4}  {:30}  {:20}".format(i,j.nombreArchivo,j.NumClusters,self.ObtenerFecha(j.fecha_crea),self.ObtenerFecha(j.fecha_modif)))


    def obtenerFecha(self,fecha):
        mes={'01':'Enero','02':'Febrero','03':'Marzo','04':'Abril','05':'Mayo','06':'Junio','07':'Julio','08':'Agosto','09':'Septiembre','10':'Octubre','11':'Noviembre','12':'Diciembre'}
        return "{:4}{:5}{:6}{:10}".format("\t"+fecha[6:8],mes.get(fecha[4:6]),fecha[0:4],fecha[8:10]+':'+fecha[10:12]+':'+fecha[12:14])

    def ruta(self):
        print("\n")
        ruta = os.getcwd()
        if 'home' in ruta:
            ruta = ruta.split('/')
            ruta = '~/' + "/".join(ruta[3:])
        sys.stdout.write('\x1b[1;3m' + ruta + '/' '\x1b[0m')
        print("\n")
        
    def ayuda(self):
        print("\n\t ======================================  ¿AYUDA? ======================================")
        print("\n\tcopyout [archivo] \"ruta\":     Copiar un archivo al sistema de archivos de nuestra computadora.")
        print("\tcopy  [archivo]:              Copiar archivo al sistema de archivos SGJC_FSYS.")
        print("\trm [archivo]:                 Eliminar un archivo especificado.")
        print("\tdesfrag:                      Realizar la desfragmentación.") 
        print("\tls:                           Mostrar contenido del directorio.")
        print("\tpwd:                          Mostrar el directorio actual.")
        print("\tmostrar:                      Mostrar los 64 espacios.\n")
        print("\tsalir:                        Salir del sistema de archivos.\n")
        
        
    
def convertir(tamanio):
        if(tamanio < 1024):
            return str(tamanio) + 'KB'
        tamanio /= 1024
        if(tamanio < 1024):
            return '{0:.1f}MB'.format(tamanio)
        tamanio /= 1024
        if(tamanio < 1024):
            return '{0:.1f}GB'.format(tamanio)
def print_line():
    user = os.environ.get('USER') + ' -> ' + os.uname()[1]
    sys.stdout.write('\x1b[1;36m' + user + '\x1b[0m')
    print('#' if('root' in user) else '$', end = ' ')
def main():
    print("\n\t", "============ 🗄  - FiUnamFS Montado! - 💾 ============","\n")
    sistema = SistemaArchivosSGJC()
    while(True):
        try:
            print_line()
            comand = input()
            while not comand:
                break
            if(comand=='ls'):
                sistema.ls()
            elif(comand=='pwd'):
                sistema.ruta()
            elif(comand=='mostrar'):
                sistema.mostrarTodo()
            elif(comand=='desfrag'):
                sistema.defrag()
            elif(comand=='ayuda'):
                sistema.ayuda()
            elif(comand[0:2] == 'rm'):
                if(comand[2:3]!=" "):
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Error en el comando, cheque el espacio!' + '\x1b[0m'+'\n\n')
                    continue
                if not comand[3:]:
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Inserte el nombre del archivo a remover' + '\x1b[0m'+'\n\n')
                    continue
                sistema.eliminar(comand[3:])
            elif(comand[0:2] == 'cpin'):
                if(comand[2:3]!=" "):
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Error en el comando, cheque el espacio!' + '\x1b[0m'+'\n\n')
                    continue
                if not comand[3:]:
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Inserte el nombre del archivo a remover' + '\x1b[0m'+'\n\n')
                    continue
                sistema.cpin(comand[3:])
            elif 'salir' in comand:
                print("\n\t============ 🖥  - FiUnamFS Desmontado! - 🗃 ============\n")
                exit(0)
            else:
                sys.stdout.write('\n\t'+'\x1b[1;31m' + '❌ Comando incorrecto. Por favor, escriba la palabra \"ayuda\"' + '\x1b[0m'+'\n\n')
        except (KeyboardInterrupt,EOFError):
            print("\n\t============ 🖥  - FiUnamFS Desmontado! - 🗃 ============\n")
            exit(0)
"""
    if(len(sys.argv)==3):
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
"""
if __name__ == '__main__':
    main()