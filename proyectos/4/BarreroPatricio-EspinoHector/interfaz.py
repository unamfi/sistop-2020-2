import sys

##Comandos
def validar_comandos(num_parametros,lista):
    nombre = sys._getframe(1).f_code.co_name
    tamano = len(lista)
    if num_parametros != tamano:
        print('{} solo recibe: #{} parametros, pero recibio: #{} '.format(
            nombre,num_parametros,tamano)
            )
        return False
    return True


def ls(*argv):
    if validar_comandos(0,argv):
        print("Mostramos los Archivos ")

def lstat(*argv):
    if validar_comandos(0,argv):
        print("Aquí estan todos tus archivos papá y sus datos")

def cp(*argv):
    if validar_comandos(2,argv):
        a,b = argv
        if ("/" in a) ^ ("/" in b):
            print("Ruta inicial {}, Ruta final {}".format(a,b))
        else:
            print("Se debe agregar una y solo una ruta de sistema\n \
La ruta del sistema debe incluir '/'")
        

def rm(*argv):
    if validar_comandos(1,argv):
        print("Eliminando archivo {}".format(argv[0]))

def cat(*argv):
    if validar_comandos(1,argv):
        print("Cat al archivo",argv[0])

def stat(*argv):
    if validar_comandos(1,argv):
        print("Mostramos los datos del archivo",argv[0])

def defrag(*argv):
    if validar_comandos(0,argv):
        print("Piri piri piri ando desframentiri")

def help(*argv):
    print(
        """Se utilizan comandos similares a posix:
Comandos:

    help
        Muestra este Menu
    ls
        Muestra los contenidos del archivo
    stat [nombre_archivo]
        Muestra los distintos datos del archivo, incluyendo:
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
    defrag
        Desfragmenta el volumen.
    exit
        Sale del programa.
        """
        )

def exit(*argv):
    print("Hasta pronto!")
    sys.exit()

def main():
    menu={"ls":ls,"lstat":lstat,"cp":cp,"help":help,"exit":exit,    
    "stat":stat,"rm":rm,"defrag":defrag,"cat":cat}
    help()
    print("Ingrese la opcion indicada")
    opcion = ""
    while True:
        opcion = input(">>> ").split()
        if opcion[0] in menu:
            menu[ opcion[0] ]( *opcion[1:] )
        else:
            print("Opcion Invalida")



if __name__ == "__main__":
    main()