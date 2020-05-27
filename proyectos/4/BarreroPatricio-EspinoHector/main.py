import sys
from colorama import init,Back,Fore
from sistema_archivos import SistemaArchivos

ubicacion_diskete = "fiunamfs.img"

##Creamos un validador, asegura que los comandos tengan el numero de parametros deseado. 
##-> Tenerlo así da mayor escalabilidad
def validar_comandos(num_parametros,lista):
    nombre = sys._getframe(1).f_code.co_name
    tamano = len(lista)
    if num_parametros != tamano:
        mostrarError('{} solo recibe: #{} parametros, pero recibio: #{} '.format(
            nombre,num_parametros,tamano)
            )
        return False
    return True

###Coloreamos las salidas
def mostrarNormal(cadena):
    print(Back.CYAN+Fore.BLACK+cadena)
def mostrarError(cadena):
    print(Fore.BLACK+Back.RED+cadena)
def prompt():
    entrada = input(Fore.GREEN + ">>> ").split()
    return entrada

sa = SistemaArchivos(ubicacion_diskete)

###Definimos el como trabajan los distintos comandos
def ls(*argv):
    if validar_comandos(0,argv):
        mostrarNormal("Mostramos los Archivos ")
        print(sa)
def lstat(*argv):
    if validar_comandos(0,argv):
        mostrarNormal("Aquí estan todos tus archivos papá y sus datos")
        print(repr(sa))
def cp(*argv):
    if validar_comandos(2,argv):
        a,b = argv
        if ("/" in a) ^ ("/" in b):
            ###Pato
            try:
                sa.copiar(a, b)
            except FileNotFoundError as f:
                mostrarError("Error: El archivo {} no existe".format(f.filename))
            except MemoryError:
                mostrarError("Error: La memoria del diskete se lleno")
            except SyntaxError:
                mostrarError("Error: El nombre {} es incorrecto")
            else:
                mostrarNormal("Se copio el archivo cuya ruta inicial es {} y la ruta final es {}".format(a,b))
        else:
            mostrarError("Se debe agregar una y solo una ruta de sistema\n \
La ruta del sistema debe incluir '/'")
        

def rm(*argv):
    if validar_comandos(1,argv):
        try:
            sa.borrar(argv[0])
        except FileNotFoundError:
            mostrarError("Error: El archivo {} no existe".format(argv[0]))
def cat(*argv):
    if validar_comandos(1,argv):
        try:
            mostrarNormal("Cat al archivo"+argv[0])
            print(sa.leer_archivo(argv[0]))
        except FileNotFoundError:
            mostrarError("Error: El archivo {} no existe".format(argv[0]))

def stat(*argv):
    if validar_comandos(1,argv):
        try:
            mostrarNormal("Mostramos los datos del archivo"+argv[0])
            print(sa.obtener_datos_archivo(argv[0]))
        except FileNotFoundError:
            mostrarError("Error: El archivo {} no existe".format(argv[0]))
        
def help(*argv):
    mostrarNormal(
        """Se utilizan comandos similares a posix. El archivo fiunamfs.img debe estar en la misma carpeta que este archivo:
Comandos:

    help
        Muestra este Menu
    ls
        Muestra los contenidos del archivo
    stat [nombre_archivo]
        Muestra los distintos initdatos del archivo, incluyendo:
            nombre,fecha de creacion, tamaño, cluster inicial, etc.
    lstat
        Muestra todos los datos de todos los archivos
    rm [nombre_archivo]
        Elimina el archivo.
    cat [nombre_archivo]
        Muestra el contenido del archivo.
    cp [origen] [destino]
        Copia desde el volumen hacía la computadora o viseversa.
            El archivo de la computadora debe tener / Ej: /imagen.jpg
            Solamente un parametro puede tener diagonal
    exit
        Sale del programa.
        """
        )

def exit(*argv):
    mostrarNormal("Hasta pronto!")
    sys.exit()

##Funcion principal, despliega el menu, parsea las entradas.
##El menú se define acorde a las entradas del usuario y manda los parametros.
##Al querer hacer una interfaz interactiva creamos un ciclo infinito.

def main():
    menu={"ls":ls,"lstat":lstat,"cp":cp,"help":help,"exit":exit,    
    "stat":stat,"rm":rm,"cat":cat}
    mostrarNormal("Ingrese el comando deseado, si necesita ayuda escriba: help")
    opcion = ""
    while True:
        opcion = prompt()
        if opcion and opcion[0] in menu:  # 
            menu[ opcion[0] ]( *opcion[1:] )
        else:
            mostrarError("Opcion Invalida")

if __name__ == "__main__":
    init(autoreset=True)
    main()