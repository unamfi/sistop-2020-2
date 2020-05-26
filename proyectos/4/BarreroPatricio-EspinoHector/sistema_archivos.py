# Importamos lo necesario

from codecs import decode

class Archivo:

    def __init__(self, cadena):
        self.nombre = cadena[:15].strip()
        self.tamano = int(cadena[16:24])
        self.cluster_inicial = int(cadena[25:30])
        self.fecha_creacion = None
        self.fecha_modificacion = None

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.nombre, self.tamano, self.cluster_inicial, 
                                          self.fecha_creacion, self.fecha_modificacion)

class SistemaArchivos:

    def __init__(self, ubicacion_diskete, nombre_original = "FiUnamFS"):
        #Comprobamos que el archivo que leemos es el correcto
        self.ubicacion_diskete = ubicacion_diskete
        nombre_sistema_archivos = self.leer(0, 8)
        if nombre_sistema_archivos != nombre_original:
            print("error")
        #Obtenemos caracteristicas del sistemade archivos
        version = self.leer(10, 3)
        etiqueta_volumen = self.leer(20, 15)
        self.tamano_cluster = int(self.leer(40, 5))
        self.num_clusters_directorio = int(self.leer(47, 2))
        num_clusters_unidad_completa = int(self.leer(52, 8))
        print("version =", version)
        print("etiqueta_volumen =", etiqueta_volumen)
        print("tamano_cluster =", self.tamano_cluster)
        print("numero de clusters directorio =", self.num_clusters_directorio)
        print("num_clusters_unidad_completa =", num_clusters_unidad_completa)

    def leer_archivos(self, tamano_archivo = 64):

        self.archivos = []
        for i in range(1, self.num_clusters_directorio+1):
            for j in range(self.tamano_cluster//tamano_archivo):
                offset = self.tamano_cluster*i + tamano_archivo*j
                cadena = self.leer(offset, tamano_archivo)
                if cadena[:15] != 'Xx.xXx.xXx.xXx.':
                    archivo = Archivo(cadena)
                    self.archivos.append(archivo)

    def leer_archivo(self, nombre):  # Puede que el nombre no exista
        for archivo in self.archivos:
            if archivo.nombre == nombre:
                return self.leer(self.tamano_cluster*archivo.cluster_inicial, archivo.tamano)

    def leer(self, inicio, cantidad, ubicacion = self.ubiacion_archivo, codificacion = "utf-8"):
        archivo = open(ubicacion, "rb+")
        archivo.seek(inicio)
        lectura = archivo.read(cantidad)
        archivo.close()
        try:
            return lectura.decode(codificacion)  # hex => str
        except:
            return lectura      

    def __str__(self):
        return '\n'.join(map(repr, self.archivos))

    def __repr__(self):
        max_nombre = 0
        #max_

ubicacion_archivo = "fiunamfs.img" 
sa = SistemaArchivos(ubicacion_archivo)
sa.leer_archivos()
print(sa.leer_archivo("logo.png"))
sa.cerrar()

#Menu
#ls: Muestra todos los arhcivos (unicamente el nombre)
#ls -l: Muestra todos los achivos (pero con todo)
#cp A B: copia el archivo en la direccion A a B
#rm A: elimina el archivo A
#cat A: Muestra el contenido A
#stat A: info del archivo A  
#defrag: desfragmenta 
#help
#exit

