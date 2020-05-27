import sys

##Comandos
def validar_comandos(funcion,num_comandos,lista):
    if num_comandos > len(lista):
        print('{} solo recive #{}comandos pero recivio #{} '.format(funcion,num_comandos,len(lista)))


def ls(*argv):
    print("Mostramos los Archivos ")

def lstat(*argv):
    print("Aquí estan todos tus archivos papá y sus datos")

def cp(*argv):
    if "\\" in a:
        a,b = b,a
    elif not "\\" in b:
        print("Ninguna de las rutas corresponde a una del sistema")
        return -1
    print("Ruta inicial {}, Ruta final{}".format(a,b))

def rm(*argv):
    print("Eliminando archivo")

def cat(*argv):
    print("Cat al archivo")

def stat(*argv):
    print("Mostramos los datos del archivo")

def defrag(*argv):
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
        if len(opcion) > 2:
            print("Demasiadas opciones  ")
        elif opcion[0] in menu:
            menu[ opcion[0] ]( *opcion[1:0] )
        else:
            print("Opcion Invalida")



if __name__ == "__main__":
    main()