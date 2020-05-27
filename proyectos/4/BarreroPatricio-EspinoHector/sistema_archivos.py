# Importamos lo necesario

from math import ceil

from fecha import formatear, fecha_actual

# 

def agregar_espacios(cadena, num):
    num_espacios =  num - len(str(cadena))
    if num_espacios <= 0:
        return cadena
    return ' ' * num_espacios + str(cadena)

# Funciones Relacionadas con Manejo de Archivos

def tamano_archivo(ubicacion):
    temp = open(ubicacion, "rb+")
    cantidad = len(temp.read())
    temp.close()
    return cantidad

def escribir(inicio, contenido, ubicacion, codificacion = "utf-8"):
    if contenido:
        contenido = bytes(contenido, codificacion)
    archivo = open(ubicacion, "rb+")
    archivo.seek(inicio)
    archivo.write(contenido)
    archivo.close()

def leer(inicio, cantidad, ubicacion, codificacion = "utf-8"):
    archivo = open(ubicacion, "rb+")
    archivo.seek(inicio)
    lectura = archivo.read(cantidad)
    archivo.close()
    try:
        return lectura.decode(codificacion)  # hex => str
    except:
        return lectura
    

class Archivo:

    def __init__(self, cadena):
        self.nombre = cadena[:15].strip()
        self.tamano = int(cadena[16:24].strip())
        self.cluster_inicial = int(cadena[25:30])
        self.fecha_creacion = cadena[31:45]
        self.fecha_modificacion = cadena[46:60]

    def __eq__(self, other):
        if type(other) != Archivo:
            return False
        return self.cluster_inicial == other.cluster_inicial

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return '{}\t{}\t{}\t{}\t{}'.format(agregar_espacios(self.nombre, 15), agregar_espacios(self.tamano, 8), 
                                        agregar_espacios(self.cluster_inicial, 15), agregar_espacios(formatear(self.fecha_creacion), 14),
                                        agregar_espacios(formatear(self.fecha_modificacion), 14))

class SistemaArchivos:

    def __init__(self, ubicacion_diskete, tamano_directorio = 64,nombre_original = "FiUnamFS"):
        #Comprobamos que el archivo que leemos es el correcto
        self.ubicacion_diskete = ubicacion_diskete
        nombre_sistema_archivos = leer(0, 8, ubicacion_diskete)
        if nombre_sistema_archivos != nombre_original:
            print("error")
        self.tamano_directorio = 64
        #Obtenemos caracteristicas del sistemade archivos
        version = leer(10, 3, ubicacion_diskete)
        etiqueta_volumen = leer(20, 15, ubicacion_diskete)
        self.tamano_cluster = int(leer(40, 5, ubicacion_diskete))
        self.num_clusters_directorio = int(leer(47, 2, ubicacion_diskete))
        num_clusters_unidad_completa = int(leer(52, 8, ubicacion_diskete))
        print("version =", version)
        print("etiqueta volumen =", etiqueta_volumen)
        print("tamano cluster =", self.tamano_cluster)
        print("numero de clusters directorio =", self.num_clusters_directorio)
        print("num clusters unidad completa =", num_clusters_unidad_completa)

    def leer_archivos(self):
        '''
        Lee el directorio  del diskete obteniendo la informacion pertinente de cada archivo (nombre, tamano, cluster_inicial, etc)
        --params--
        int tamano_directorio - indica el tamaño de la informacion de cada directorio
        '''
        self.archivos = []
        for i in range(1, self.num_clusters_directorio+1):
            for j in range(self.tamano_cluster//self.tamano_directorio):
                offset = self.tamano_cluster*i + self.tamano_directorio*j
                cadena = leer(offset, self.tamano_directorio, self.ubicacion_diskete)
                if cadena[:15] != 'Xx.xXx.xXx.xXx.':  # Excluimos los archivos vacios
                    archivo = Archivo(cadena)
                    self.archivos.append(archivo)

    def obtener_archivo(self, nombre):
        self.leer_archivos()
        for archivo in self.archivos:
            if archivo.nombre == nombre:
                return archivo
        raise FileNotFoundError

    def leer_archivo(self, nombre):  # Puede que el nombre no exista
        archivo = self.obtener_archivo(nombre)
        inicio = self.tamano_cluster*archivo.cluster_inicial
        tamano = archivo.tamano
        return leer(inicio, tamano, self.ubicacion_diskete)

    def entrada_directorio(self, nombre = 'Xx.xXx.xXx.xXx.'):
        """
        Busca en el directorio del diskete la entrada correspondiente al archivo con el nombre "nombre" 
        --returns--
        int offset - offset correspondiente para almacenar los datos del archivo en el directorio
        None si no hay espacio disponible
        """
        for i in range(1, self.num_clusters_directorio+1):
            for j in range(self.tamano_cluster//self.tamano_directorio):
                offset = self.tamano_cluster*i + self.tamano_directorio*j
                cadena = leer(offset, self.tamano_directorio, self.ubicacion_diskete)
                if cadena[:15].strip() == nombre: 
                    return offset
        raise MemoryError

    def localidad_vacia(self, tamano):
        """
        Obtiene el cluster inicial en el espacio de datos que sea lo suficientemente grande para almacenar de forma contigua el contenido de un archivo de tamaño tamano
        --params--
        int tamano - el tamano de un archivo a guardar
        --returns--
        int cluster_incial - cluster inicial deseado para almacenar el archivo en curso
        """
        for a, b in zip(self.archivos, self.archivos[1:]):
            inicio = a.tamano + a.inicio // self.tamano_cluster
            if b.inicio - inicio >= tamano:
                return inicio

    def escribir_en_directorios(self, nombre, tamano):
        offset = self.entrada_directorio()
        cluster_inicial = str(self.localidad_vacia(tamano))
        nombre = agregar_espacios(nombre, 15)
        cluster_inicial = agregar_espacios(cluster_inicial, 5)
        tamano = agregar_espacios(str(tamano), 8)
        fecha_creacion = fecha_actual() 
        escribir(offset, nombre + tamano + cluster_inicial + fecha_creacion + fecha_creacion, self.ubicacion_diskete)
        return cluster_inicial

    def escribir_archivo_diskete(self, nombre, contenido):
        """
        Permite escribir un archivo en el disket

        Si en el disket se encuentra un archivo con nombre se sobreescribe el contenido
        Si en el disket no encuentra un archivo con nombre crea un archivo nuevo si es posible (reviar returns)
        --params--
        str nombre - nombre del archivo que deseamos escribir
        str contenido - lo que queremos escribir en el archivo
        --returns--
        0 - si el nombre del archivo es incorrecto
        1 - si la memoria esta llena
        2 - si la capacidad de archivos es la maxima
        3 - si la operacion fue un exito
        """
        nombre_correcto(nombre)
        archivo = self.obtener_archivo(nombre)
        tamano = len(contenido)
        inicio = 0
        if archivo == None:  # Si no existe el archivo en el directorio
            inicio =  self.escribir_en_directorios(nombre, tamano)
        else:
            if tamano > archivo.tamano:
                inicio =  self.escribir_en_directorios(nombre, tamano)
            else:  # Actualizar fecha y tamano
                offset = self.entrada_directorio(archivo.nombre)
                tamano = agregar_espacios(str(tamano), 8)
                fecha_modificacion = fecha_actual() 
                escribir(offset, nombre + tamano + archivo.cluster_inicial + archivo.fecha_creacion + fecha_modificacion, self.ubicacion_diskete)
                inicio =  archivo.cluster_inicial
        escribir(inicio, contenido, self.ubicacion_diskete)
    
    def copiar(self, archivo1, archivo2):  # Copia el archivo1 en el archivo2
        """
        Copia el contenido del archivo1 en la direccion archivo2
        --params--
        str archivo1 - Ubicacion del archivo1
        str archivo2 - ubiacion del archivo2
        """
        self.leer_archivos()
        if '/' in archivo1:
            contenido = leer(0, tamano_archivo(archivo1), archivo1)  #hacer verificacion
            self.escribir_archivo_diskete(archivo2, contenido)
        else:
            contenido = self.leer_archivo(archivo1)  # Verificar esto
            escribir(0, contenido, archivo2, codificacion=None)

    def borrar(self, nombre_archivo):
        self.leer_archivos()
        archivo = self.obtener_archivo(nombre_archivo)
        offset = self.entrada_directorio(archivo.nombre)
        contenido = 'Xx.xXx.xXx.xXx..00000000.00000.00000000000000.00000000000000....'
        print(offset)
        escribir(offset, contenido, self.ubicacion_diskete)

    def __str__(self):
        self.leer_archivos()
        nombre_archivo = agregar_espacios("Nombre Archivo", 15)
        tamano = agregar_espacios("Tamaño Bytes", 8)
        cluster_inicial = agregar_espacios("Cluster Inicial", 15)
        fecha_creacion = agregar_espacios("Fecha Creacion", 14)
        fecha_modificacion = agregar_espacios("Fecha Modificacion", 14)
        print("{}\t{}\t{}\t{}\t\t{}".format(nombre_archivo, tamano, cluster_inicial, fecha_creacion, fecha_modificacion))
        return '\n'.join(map(repr, self.archivos))

    def __repr__(self):
        max_nombre = 0
        #max_

ubicacion_archivo = "fiunamfs.img" 
sa = SistemaArchivos(ubicacion_archivo)
sa.leer_archivos()
#sa.borrar("logo.png")
print(sa)



