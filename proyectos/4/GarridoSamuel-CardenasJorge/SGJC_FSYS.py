import mmap
import os
import sys
import os.path, time
import math
import re

class SuperBloque:
    tamanio_entrada = 64
    def __init__(self):
        try:
            self.f = open('fiunamfs.img','r+b')
            self.imagen = mmap.mmap(self.f.fileno(),0,access=mmap.ACCESS_READ)
            self.nombre             = self.imagen[0:8].decode('ASCII')      
            self.version            = self.imagen[10:13].decode('ASCII')
            self.etiqueta_volumen   = self.imagen[20:35].decode('ASCII')
            self.tamanio_cluster    = int(self.imagen[40:45].decode('ASCII'))
            self.num_cluster        = int(self.imagen[47:49].decode('ASCII'))
            self.total_clusters     = int(self.imagen[52:60].decode('ASCII'))                       
            self.f.close()
            self.imagen.close()
        except IOError:
            print("Error al abrir el sistema de archivos ")

class Entrada:
    nombre_archivo = 15
    tamanio_archivo = 8
    num_cluster = 5
    fechaCreacion = 14
    fecha_modificacion = 14

    def __init__(self, entrada):
        self.nombreArchivo   = entrada[0:15].decode('ASCII').lstrip()
        self.tamanoArchivo   = int(entrada[16:24].decode('ASCII'))
        self.NumClusters     = int(entrada[25:30].decode('ASCII'))
        self.fecha_crea      = entrada[31:45].decode('ASCII')
        self.fecha_modif     = entrada[46:60].decode('ASCII')
        self.numeroDireccion = 0


class SistemaArchivosSGJC:
    SuperBloque = SuperBloque()
    archivo = open('fiunamfs.img','a+b')
    imagen = mmap.mmap(archivo.fileno(),0,access=mmap.ACCESS_WRITE)
    sinUsar ='Xx.xXx.xXx.xXx.'

    def inodo(self):
        inodos = []
        for i in range(SuperBloque.tamanio_entrada):
            inicio = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada
            fin = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada + self.SuperBloque.tamanio_entrada
            insercion = Entrada(self.imagen[inicio:fin])
            if self.sinUsar != insercion.nombreArchivo:
                insercion.numeroDireccion = i
                inodos.append(insercion)
        return inodos

    def buscar (self,archivo):
        for i in range(SuperBloque.tamanio_entrada):
            inicio = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada
            fin = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada + self.SuperBloque.tamanio_entrada
            busqueda = Entrada(self.imagen[inicio:fin])
            if archivo == busqueda.nombreArchivo:
                busqueda.numeroDireccion = i
                return busqueda

    def registrar(self,archivo,cluster):
        for i in range(SuperBloque.tamanio_entrada):
            inicio = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada
            fin = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada + self.SuperBloque.tamanio_entrada
            registro = Entrada(self.imagen[inicio:fin])
            if self.sinUsar == registro.nombreArchivo:                                                                
                self.imagen[inicio:inicio + registro.nombre_archivo] = archivo.rjust(registro.nombre_archivo).encode('ASCII')
                archivo_tamanio = str(os.stat(archivo).st_size)
                nuevo_p = inicio + registro.nombre_archivo + 1
                self.imagen[nuevo_p :nuevo_p + registro.tamanio_archivo] = archivo_tamanio.zfill(registro.tamanio_archivo).encode('ASCII')
                cluster_archivo = str(cluster)              
                nuevo_p += registro.tamanio_archivo + 1
                self.imagen[nuevo_p:nuevo_p + registro.num_cluster] = cluster_archivo.zfill(registro.num_cluster).encode('ASCII')
                fecha_creacion= time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getctime(archivo)))
                nuevo_p += registro.num_cluster + 1
                self.imagen[nuevo_p:nuevo_p + registro.fechaCreacion] = fecha_creacion.encode('ASCII')
                fecha_modif=time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(archivo)))
                nuevo_p += registro.fechaCreacion + 1
                self.imagen[nuevo_p:nuevo_p + registro.fecha_modificacion] = fecha_modif.encode('ASCII')
                break

    def ls(self):
        print("Nombre  Cluster  Tamaño   Fecha y hora de Modificación   Fecha y hora de creación")
        for i in self.inodo():
            tamanioArchivo = convertir(i.tamanoArchivo)
            fecha_c= self.obtenerFecha(i.fecha_crea)
            fecha_m = self.obtenerFecha(i.fecha_modif)
            print(i.nombreArchivo, i.NumClusters, tamanioArchivo, fecha_c,fecha_m)
    
    def eliminar(self,archivo):
        busqueda = self.buscar(archivo)
        if busqueda is not None:
            archivoEliminar = self.SuperBloque.tamanio_cluster + self.SuperBloque.tamanio_entrada *busqueda.numeroDireccion
            self.imagen[archivoEliminar:archivoEliminar + busqueda.nombre_archivo] = bytes(self.sinUsar,'ASCII')
            self.imagen[archivoEliminar+16:archivoEliminar+24]=bytes("00000000",'ASCII')
            self.imagen[archivoEliminar+25:archivoEliminar+30]=bytes("00000",'ASCII')
            self.imagen[archivoEliminar+31:archivoEliminar+45]=bytes('00000000000000','ASCII')
            self.imagen[archivoEliminar+46:archivoEliminar+60]=bytes('00000000000000','ASCII')
            
        else :
            print("El archivo no existe en el sistema.")

    def cpout(self,archivo):
        i = self.buscar(archivo)
        if i is not None :
            p = self.SuperBloque.tamanio_cluster + self.SuperBloque.tamanio_entrada * i.numeroDireccion
            archivocp = open(archivo,"a+b")
            cluster = self.SuperBloque.tamanio_cluster * i.NumClusters
            archivocp.write(self.imagen[cluster:cluster + i.tamanoArchivo])
            archivocp.close()
        else:
            print(i.nombreArchivo + " : Archivo no encontrado ")

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


    def Copiar(self, archivo):
        inodos = self.inodo()
        inodos.sort(key = lambda x : x.NumClusters)
        tam_archivo = os.stat(archivo).st_size
        cluster_archivo = math.ceil(tam_archivo/self.SuperBloque.tamanio_cluster)

        if len(inodos) == 0:
            if  cluster_archivo <= (self.SuperBloque.total_clusters - 4):
                f = open(archivo,"rb")
                #lo meteremos en el cluster 5
                destino = self.SuperBloque.tamanio_cluster * 5
                self.imagen[destino: destino + tam_archivo] = f.read()
                self.registrar(archivo,5)
                f.close()
            else:
                print("Archivo demasiado grande :(")
        else:
            copiado = False
            for j in range(0,len(inodos)-1):
                ultimo_cluster = inodos[j].NumClusters + math.ceil( inodos[j].tamanoArchivo / self.SuperBloque.tamanio_cluster)
                espacio_entre_sig_archivo = inodos[j+1].NumClusters - ultimo_cluster

                if cluster_archivo <= espacio_entre_sig_archivo:
                    f = open(archivo, "rb")
                    p = int(self.SuperBloque.tamanio_cluster * (cluster_archivo + 1))
                    self.imagen[p : p + tam_archivo ] = f.read()
                    self.registrar(archivo,cluster_archivo + 1)
                    f.close()
                    copiado = True
                    break

            if copiado == False:
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
                    print("Archivo demasido grande :(")
    #Método para desfragmentar 
    def defrag(self):
        for i in range(SuperBloque.tamanio_entrada): 
            p = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada
            j = Entrada(self.imagen[p:p + self.SuperBloque.tamanio_entrada])
            #print("{} + {} + {}".format(i,j.nombreArchivo,j.NumClusters))
            if (j.nombreArchivo==self.sinUsar):
                for k in range (i+1,SuperBloque.tamanio_entrada):
                    paux = self.SuperBloque.tamanio_cluster + k * self.SuperBloque.tamanio_entrada
                    jaux = Entrada(self.imagen[paux:paux + self.SuperBloque.tamanio_entrada])
                    if(jaux.nombreArchivo!=self.sinUsar):
                        self.imagen[p:p + self.SuperBloque.tamanio_entrada]=self.imagen[paux:paux + self.SuperBloque.tamanio_entrada]
                        self.imagen[paux:paux + 15]=bytes(self.sinUsar,'ASCII')
                        self.imagen[paux+16:paux+24]=bytes("".zfill(8),'ASCII')
                        self.imagen[paux+25:paux+30]=bytes("".zfill(5),'ASCII')
                        self.imagen[paux+31:paux+45]=bytes("".zfill(14),'ASCII')
                        self.imagen[paux+46:paux+60]=bytes("".zfill(14),'ASCII')
                        break
        sys.stdout.write('\n\t'+'\x1b[1;32m' + 'Desfragmentación completa! :) ' + '\x1b[0m'+'\n\n')


    def mostrarTodo(self):
        print("IN  Nombre archivo   cluster  Fecha de creación      \t      Fecha de modificación")
        for i in range (SuperBloque.tamanio_entrada):
            p = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada
            j = Entrada(self.imagen[p:p + self.SuperBloque.tamanio_entrada])
            if j.nombreArchivo == self.sinUsar:
                print("{:2}  {:15}     {:4}  {:30}  {:20}".format(i,j.nombreArchivo,j.NumClusters,j.fecha_crea,j.fecha_modif))
            else:
                print("{:2}  {:15}     {:4}  {:30}  {:20}".format(i,j.nombreArchivo,j.NumClusters,self.obtenerFecha(j.fecha_crea),self.obtenerFecha(j.fecha_modif)))


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
    SGJC = SistemaArchivosSGJC()
    breaker = False
    while(True):
        try:
            print_line()
            comand = input()
            romper = False
            while not comand:
                romper = True
            if romper:
                break
            elif(comand=='ayuda'):
                SGJC.ayuda()
            if(comand=='ls'):
                SGJC.ls()
            elif(comand=='pwd'):
                SGJC.ruta()
            elif(comand=='mostrar'):
                SGJC.mostrarTodo()
            elif(comand=='desfrag'):
                SGJC.defrag()
            
            elif(comand[0:2] == 'rm'):
                if(comand[2:3]!=" "):
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Error en el comando, cheque el espacio!' + '\x1b[0m'+'\n\n')
                    continue
                if not comand[3:]:
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Inserte el nombre del archivo a remover' + '\x1b[0m'+'\n\n')
                    continue
                SGJC.eliminar(comand[3:])
            elif(comand[0:3] == 'cpi'):
                if(comand[3:4]!=" "):
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Error en el comando, cheque el espacio!' + '\x1b[0m'+'\n\n')
                    continue
                if not comand[4:]:
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Inserte el nombre del archivo a remover' + '\x1b[0m'+'\n\n')
                    continue
                SGJC.cpin(comand[4:])
            elif(comand[0:3] == 'cpo'):
                if(comand[3:4]!=" "):
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Error en el comando, cheque el espacio!' + '\x1b[0m'+'\n\n')
                    continue
                if not comand[4:]:
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Inserte el nombre del archivo a remover' + '\x1b[0m'+'\n\n')
                    continue
                SGJC.cpout(comand[4:])
            elif 'salir' in comand:
                print("\n\t============ 🖥  - FiUnamFS Desmontado! - 🗃 ============\n")
                exit(0)
            else:
                sys.stdout.write('\n\t'+'\x1b[1;31m' + '❌ Comando incorrecto. Por favor, escriba la palabra \"ayuda\"' + '\x1b[0m'+'\n\n')
        except (KeyboardInterrupt,EOFError):
            print("\n\t============ 🖥  - FiUnamFS Desmontado! - 🗃 ============\n")
            exit(0)
if __name__ == '__main__':
    main()