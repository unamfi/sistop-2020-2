import mmap
import math
import os
import sys
import os.path, time
import re
## Mecionamos la codificación que usaremos, en el caso de nuestro ejercicio es ASCII
codificacion = 'ASCII'
class SuperBloque:
    tamanio_entrada = 64
    def __init__(self):
        ##Intentamos abrir la imagen del sistema de archivos
        try:
            ## Usamos mmap para tratar con el acceso al sistema de archivos y luego dividimos
            ## Este sector en los que corresponderá el nombre, la versión, el tamaño de cluster, el número de clusters
            self.f = open('fiunamfs.img','r+b')
            self.imagen = mmap.mmap(self.f.fileno(),0,access=mmap.ACCESS_READ)
            self.nombre             = self.imagen[0:8].decode(codificacion)      
            self.version            = self.imagen[10:13].decode(codificacion)
            self.etiqueta_volumen   = self.imagen[20:35].decode(codificacion)
            self.tamanio_cluster    = int(self.imagen[40:45].decode(codificacion))
            self.num_cluster        = int(self.imagen[47:49].decode(codificacion))
            self.total_clusters     = int(self.imagen[52:60].decode(codificacion))                       
            self.f.close()
            self.imagen.close()
        except IOError:
            print("Error al abrir el sistema de archivos ")

class Entrada:
    #La clase entrada sirve para la tener la información de las secciones que se necesitan para que funcione el sistema de archivos
    nombre_archivo = 15
    tamanio_archivo = 8
    num_cluster = 5
    fechaCreacion = 14
    fecha_modificacion = 14
    ##Inicializamos los elementos de metadata que queremos en nuestros bloques
    def __init__(self, entrada):
        self.nombreArchivo   = entrada[0:15].decode(codificacion).lstrip()
        self.tamanoArchivo   = int(entrada[16:24].decode(codificacion))
        self.NumClusters     = int(entrada[25:30].decode(codificacion))
        self.fecha_crea      = entrada[31:45].decode(codificacion)
        self.fecha_modif     = entrada[46:60].decode(codificacion)
        self.numeroDireccion = 0

##Clase de nuestro sistema de archivos
class SistemaArchivosSGJC:
    SuperBloque = SuperBloque()
    archivo = open('fiunamfs.img','a+b') ##Abrimos la imagen y la pasamos a mmap para que se encarge de secionarla por nosotros.
    imagen = mmap.mmap(archivo.fileno(),0,access=mmap.ACCESS_WRITE)
    sinUsar ='Xx.xXx.xXx.xXx.'

    def inodo(self):
        inodos = []
        ## Generamos los inodos donde el bloque que no podemos usar es el 0, al recorrernos al primero vamos hasta tener las 64 entradas
        for i in range(SuperBloque.tamanio_entrada):
            inicio = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada
            fin = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada + self.SuperBloque.tamanio_entrada
            insercion = Entrada(self.imagen[inicio:fin])
            ##Cada vez que nos encontremos con una sección con Xx.xXx.xXx.xXx. significa que estamos dándole pauta para referirse a ese bloque como un i nodo
            if self.sinUsar != insercion.nombreArchivo:
                insercion.numeroDireccion = i
                inodos.append(insercion)
        return inodos

    def buscar (self,archivo):
        for i in range(SuperBloque.tamanio_entrada):
            ##Recorremos todo dentro de superbloque por los clusters esperando a sacar todos los nombre dentro de ellos.
            ## Comparamos si es que un archivo tiene el mismo nombre y si es así hemos encontrado una coincidencia
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
                ##Para poder registrar un elemento vamos a estrucuturarlo en vase al tamano y donde deben ir los elementos dados los bloques                                                                
                self.imagen[inicio:inicio + registro.nombre_archivo] = archivo.rjust(registro.nombre_archivo).encode(codificacion)
                archivo_tamanio = str(os.stat(archivo).st_size)
                espacio = inicio + registro.nombre_archivo + 1
                ##Colocamos el tamaño del archivo al extraerlo
                self.imagen[espacio :espacio + registro.tamanio_archivo] = archivo_tamanio.zfill(registro.tamanio_archivo).encode(codificacion)
                cluster_archivo = str(cluster)              
                espacio += registro.tamanio_archivo + 1
                ## El número de clusters que necesitará si llena uno
                self.imagen[espacio:espacio + registro.num_cluster] = cluster_archivo.zfill(registro.num_cluster).encode(codificacion)
                fecha_creacion= time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getctime(archivo)))
                espacio += registro.num_cluster + 1
                ## La fecha y hora de creación con la función gmtime de time podemos optenerlas para registrarlas
                self.imagen[espacio:espacio + registro.fechaCreacion] = fecha_creacion.encode(codificacion)
                fecha_modif=time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(archivo)))
                espacio += registro.fechaCreacion + 1
                ##Una vez que hemos armado todo el proceso de ensamble de un bloque, procedemos no seguir recorriendo el superbloque
                self.imagen[espacio:espacio + registro.fecha_modificacion] = fecha_modif.encode(codificacion)
                break
    def ls(self):
        print("Nombre           Cluster    Tamaño              Fecha de creación               Fecha de modificación")
        for nodo in self.inodo():
            ## Dado que ya sabemos la ubicación de la inicialización de estos archivos, podemos llamarlos a través del arreglo de inodos
            tamanioArchivo = convertir(nodo.tamanoArchivo)
            print("{:15}{:9}    {:12}{:24}{:24}".format(nodo.nombreArchivo, nodo.NumClusters, tamanioArchivo, self.obtenerFecha(nodo.fecha_crea),self.obtenerFecha(nodo.fecha_modif)))
    
    def eliminar(self,archivo):
        busqueda = self.buscar(archivo)
        ## Para eliminar primero buscamos coindicencias y si existen empezamos por la dirección que tenga y 60 espacios serán rellenados con ceros
        if busqueda is not None:
            archivoEliminar = self.SuperBloque.tamanio_cluster + self.SuperBloque.tamanio_entrada *busqueda.numeroDireccion
            self.imagen[archivoEliminar:archivoEliminar + busqueda.nombre_archivo] = bytes(self.sinUsar,codificacion)
            self.imagen[archivoEliminar+16:archivoEliminar+24]=bytes('00000000',codificacion)
            self.imagen[archivoEliminar+25:archivoEliminar+30]=bytes('00000',codificacion)
            self.imagen[archivoEliminar+31:archivoEliminar+45]=bytes('00000000000000',codificacion)
            self.imagen[archivoEliminar+46:archivoEliminar+60]=bytes('00000000000000',codificacion)
            sys.stdout.write('\n\t'+'\x1b[1;32m' + 'Archivo removido con éxito :)' + '\x1b[0m'+'\n\n')
            ## si hay algún pro
        else :
            sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Problemas al ubicar al archivo :c' + '\x1b[0m'+'\n\n')

    def CopiarDesde(self,archivo):
        ## Si contamos con el archivo para sacarlo, seleccionamos el espacio donde se encuentre de inicio a fin 
        ## y escribimos la sección de la imagen que contenga ese archivo
        if self.buscar(archivo) is not None:
            archivocopy = open(archivo,"a+b")
            cluster = self.SuperBloque.tamanio_cluster * self.buscar(archivo).NumClusters
            archivocopy.write(self.imagen[cluster:cluster + self.buscar(archivo).tamanoArchivo])
            archivocopy.close()
            sys.stdout.write('\n\t'+'\x1b[1;32m' + 'Archivo copiado con éxito :)' + '\x1b[0m'+'\n\n')
        else:
            sys.stdout.write('\n\t'+'\x1b[1;33m' + 'No se encuentra el archivo' + '\x1b[0m'+'\n\n')

    def CopiarHacia(self, archivo):
        if os.path.isfile(archivo):
            if len(archivo) < 15:## Verificamos que el nombre sea menor a 15 caracteres
                if self.buscar(archivo) != None:
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Archivos con el mismo nombre, favor de cambiarlo' + '\x1b[0m'+'\n\n')
                else:
                    inodos = self.inodo()##Nos apoyamos de los inodos para saber donde se ubican
                    inodos.sort(key = lambda x : x.NumClusters)
                    tam_archivo = os.stat(archivo).st_size
                    cluster_archivo = math.ceil(tam_archivo/self.SuperBloque.tamanio_cluster)
                    if len(inodos) == 0:##Empezamos con la escritura al mandarle la tarea a la función registrar
                        if  cluster_archivo <= (self.SuperBloque.total_clusters - 4):
                            f = open(archivo,"rb")
                            destino = self.SuperBloque.tamanio_cluster * 5
                            self.imagen[destino: destino + tam_archivo] = f.read()
                            self.registrar(archivo,5)
                            f.close()
                        else:
                            sys.stdout.write('\n\t'+'\x1b[1;31m' + 'Archivo demasiado grande :c' + '\x1b[0m'+'\n\n')
                    else:
                        copiado = False
                        for j in range(0,len(inodos)-1):
                            ultimo_cluster = inodos[j].NumClusters + math.ceil( inodos[j].tamanoArchivo / self.SuperBloque.tamanio_cluster)
                            espacio_siguiente_archivo = inodos[j+1].NumClusters - ultimo_cluster
                            ## Si podemos meterlo al principio lo intentamos
                            if cluster_archivo <= espacio_siguiente_archivo:
                                file = open(archivo, "rb")
                                self.imagen[int(self.SuperBloque.tamanio_cluster * (cluster_archivo + 1)) : int(self.SuperBloque.tamanio_cluster * (cluster_archivo + 1)) + tam_archivo ] = file.read()
                                self.registrar(archivo,cluster_archivo + 1)
                                file.close()
                                copiado = True
                                sys.stdout.write('\n\t'+'\x1b[1;32m' + 'Archivo copiado con éxito :)' + '\x1b[0m'+'\n\n')
                                break
                            if copiado == False:##En caso que no se haya copiado, ya que no se haya podido meter al prinicpio intentamos en los sigueintes espacios
                                ultimoEspacio = inodos[len(inodos) - 1].NumClusters + math.ceil(inodos[len(inodos) - 1].tamanoArchivo / self.SuperBloque.tamanio_cluster )
                                if cluster_archivo <= self.SuperBloque.total_clusters - ultimoEspacio:
                                    file = open(archivo,"rb")
                                    self.imagen[self.SuperBloque.total_clusters * (ultimoEspacio + 1) : self.SuperBloque.total_clusters * (ultimoEspacio + 1) + tam_archivo] = file.read()
                                    self.registrar(archivo, ultimoEspacio + 1)
                                    file.close()
                                    copiado = True
                                    sys.stdout.write('\n\t'+'\x1b[1;32m' + 'Archivo copiado con éxito :)' + '\x1b[0m'+'\n\n')
                                else:
                                    sys.stdout.write('\n\t'+'\x1b[1;31m' + 'Archivo demasiado grande :c' + '\x1b[0m'+'\n\n')

            else:
                sys.stdout.write('\n\t'+'\x1b[1;33m' + 'El nombre es demasiado grande, favor de cambiarlo' + '\x1b[0m'+'\n\n')
        else:
            sys.stdout.write('\n\t'+'\x1b[1;33m' + 'No se encuentra el archivo' + '\x1b[0m'+'\n\n')

   ##Método de desfragmentar, que consiste en recorrer los elementos y rellenar de 0 mientras recorre a las regiones superiores
    def desfragmentar(self):
        for i in range(SuperBloque.tamanio_entrada): 
            j = Entrada(self.imagen[self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada:self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada + self.SuperBloque.tamanio_entrada])
            if (j.nombreArchivo==self.sinUsar):
                for k in range (i+1,SuperBloque.tamanio_entrada):
                    pedazoMover = self.SuperBloque.tamanio_cluster + k * self.SuperBloque.tamanio_entrada
                    PedazoBorrar = Entrada(self.imagen[pedazoMover:pedazoMover + self.SuperBloque.tamanio_entrada])
                    if(PedazoBorrar.nombreArchivo!=self.sinUsar):
                        self.imagen[self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada:self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada + self.SuperBloque.tamanio_entrada]=self.imagen[pedazoMover:pedazoMover + self.SuperBloque.tamanio_entrada]
                        self.imagen[pedazoMover:pedazoMover + 15]=bytes(self.sinUsar,codificacion)
                        self.imagen[pedazoMover+16:pedazoMover+24]=bytes('00000000',codificacion)
                        self.imagen[pedazoMover+25:pedazoMover+30]=bytes('00000',codificacion)
                        self.imagen[pedazoMover+31:pedazoMover+45]=bytes('00000000000000',codificacion)
                        self.imagen[pedazoMover+46:pedazoMover+60]=bytes('00000000000000',codificacion)
                        break
        sys.stdout.write('\n\t'+'\x1b[1;32m' + 'Desfragmentación completa! :) ' + '\x1b[0m'+'\n\n')

    ## mostrar el mapeo de la imagen, para ver la ubicación exacta y si hay fragmentación
    def mostrarTodo(self):
        print("IN  Nombre archivo   cluster  Fecha de creación      \t      Fecha de modificación")
        for i in range (SuperBloque.tamanio_entrada):
            p = self.SuperBloque.tamanio_cluster + i * self.SuperBloque.tamanio_entrada
            j = Entrada(self.imagen[p:p + self.SuperBloque.tamanio_entrada])
            if j.nombreArchivo == self.sinUsar:
                print("{:2}  {:15}     {:4}  {:30}  {:20}".format(i,j.nombreArchivo,j.NumClusters,j.fecha_crea,j.fecha_modif))
            else:
                print("{:2}  {:15}     {:4}  {:30}  {:20}".format(i,j.nombreArchivo,j.NumClusters,self.obtenerFecha(j.fecha_crea),self.obtenerFecha(j.fecha_modif)))

    ## Mejorar la presentación de la fecha al mostrar la metadata de los archivos
    def obtenerFecha(self,fecha):
        mes={'01':'Enero','02':'Febrero','03':'Marzo','04':'Abril','05':'Mayo','06':'Junio','07':'Julio','08':'Agosto','09':'Septiembre','10':'Octubre','11':'Noviembre','12':'Diciembre'}
        return "{:4}{:5}{:6}{:10}".format("\t"+fecha[6:8],mes.get(fecha[4:6]),fecha[0:4],fecha[8:10]+':'+fecha[10:12]+':'+fecha[12:14])
    ## Para definir una ruta para ser usada en el método pwd
    def ruta(self):
        print("\n")
        ruta = os.getcwd()
        if 'home' in ruta:
            ruta = ruta.split('/')
            ruta = '~/' + "/".join(ruta[3:])
        sys.stdout.write('\x1b[1;3m' + ruta + '/' '\x1b[0m')
        print("\n")
        ##Función de ayuda
    def ayuda(self):
        print("\n\t ======================================  ¿AYUDA? ======================================")
        print("\n\tcpo [archivo]:                Copiar un archivo al sistema de archivos de nuestra computadora.")
        print("\tcpi  [archivo]:               Copiar archivo al sistema de archivos SGJC_FSYS.")
        print("\trm [archivo]:                 Eliminar un archivo especificado.")
        print("\tdesfrag:                      Realizar la desfragmentación.") 
        print("\tls:                           Mostrar contenido del directorio.")
        print("\tpwd:                          Mostrar el directorio actual.")
        print("\tmostrar:                      Mostrar los 64 espacios.\n")
        print("\tsalir:                        Salir del sistema de archivos.\n")
        
        
##Método de conversión de unidades de datos
def convertir(tamanio):
        if(tamanio < 1024):
            return str(tamanio) + 'KB'
        tamanio /= 1024
        if(tamanio < 1024):
            return '{0:.1f}MB'.format(tamanio)
        tamanio /= 1024
        if(tamanio < 1024):
            return '{0:.1f}GB'.format(tamanio)
## Prompt de nuestra terminal personalizada
def print_line():
    user = os.environ.get('USER') + ' -> ' + os.uname()[1]
    sys.stdout.write('\x1b[1;36m' + user + '\x1b[0m')
    print('#' if('root' in user) else '$', end = ' ')
def main():
    print("\n\t", "============ 🗄  - FiUnamFS Montado! - 💾 ============","\n")
    SGJC = SistemaArchivosSGJC()
    breaker = False
    while(True): ##Para repetir el prompt en caso que se coloque enter + enter + enter etc.
        try:
            print_line()
            comand = input()
            romper = False ## Para sacar el While superior y no imprimir lo demás abajo
            while not comand:
                romper = True
                break
            if romper:##Tenemos las opciones y las mandamos a llamar según se inserte en input()
                continue
            if(comand=='ls'):
                SGJC.ls()
            elif(comand=='desfrag'):
                SGJC.desfragmentar()
            elif(comand=='ayuda'):
                SGJC.ayuda()
            elif(comand=='pwd'):
                SGJC.ruta()
            elif(comand=='mostrar'):
                SGJC.mostrarTodo()
            elif(comand[0:2] == 'rm'): ## Elegimos comandos de 2 caracteres para poder decirle al usuari si le faltó espacio o los argumentos
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
                SGJC.CopiarHacia(comand[4:])
            elif(comand[0:3] == 'cpo'):
                if(comand[3:4]!=" "):
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Error en el comando, cheque el espacio!' + '\x1b[0m'+'\n\n')
                    continue
                if not comand[4:]:
                    sys.stdout.write('\n\t'+'\x1b[1;33m' + 'Inserte el nombre del archivo a remover' + '\x1b[0m'+'\n\n')
                    continue
                SGJC.CopiarDesde(comand[4:])
            elif 'salir' in comand: ## el comando salir es el que logra sacarnos de nuestro programa de sistema de archivos
                print("\n\t============ 🖥  - FiUnamFS Desmontado! - 🗃 ============\n")
                exit(0)
            else:
                sys.stdout.write('\n\t'+'\x1b[1;31m' + '❌ Comando incorrecto. Por favor, escriba la palabra \"ayuda\"' + '\x1b[0m'+'\n\n')
        except (KeyboardInterrupt,EOFError): ##Para poder salir con ^C o ^D sin hacer brincar una excepción
            print("\n\t============ 🖥  - FiUnamFS Desmontado! - 🗃 ============\n")
            exit(0)
if __name__ == '__main__':
    main()