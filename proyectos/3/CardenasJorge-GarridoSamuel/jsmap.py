#!/usr/bin/python3

import re
import sys
import os

# Función que genera el MAP de un proceso:
def map(pid):
    try:
        # Se abre el archivo /proc/pid/maps para obtener la informacion del proceso
        with open('/proc/' + pid + '/maps' , 'r') as file:
            buffer = [] # Arreglo donde se almacenara cada linea generada por el MAP.
            # El archivo /proc/pid/cmdline contiene el nombre del proceso:
            with open('/proc/' + pid + '/cmdline' , 'r') as f_name:
                name = f_name.readline()
                if(not name): # Si el proceso no tiene nombre, se finaliza ya que no es accesible el proceso
                    exit(0)
                # De lo contrario se imprime el nombre del proceso y la cabecera de la tabla:
                print(pid + ':\t' + name)
                print('{0:12s} {1:9s} - {2:9s} ( {3:6s} , {4:6s} ) {5:4s} {6:s}'.format(
                    '     Uso'.ljust(12), ' De pág', '  A pág', ' Size', '   Núm Pág ', 'Modo', 'Mapping'))
            # Para cada linea del archivo:
            for line in file:
                # Mediante el uso expresiones regulares se obtienen las columnas a mostrar en el map
                paginas = re.findall('[0-9a-f]+', line)[0:2]
                # Se omiten los ultimos tres digitos de la direccion
                # equivalentes a los 4KB de una pagina
                # siendo que cada posible dirección equivale a una página nueva
                pag0 = paginas[0][0:-3]
                pag1 = paginas[1][0:-3]
                # El número de paginas es igual a la direccion de la pág 1, 
                # menos la dirección de la pág 0, 
                # El tamaño de pagina se considera por defecto como 4KB
                numPag = int(pag1,16) - int(pag0,16)
                # Si se multiplica por 4 (lo equivalnte a 4KB) 
                # el número de páginas, obtiene el tamaño de cada sección
                size = convertir(numPag * 4)
                # Los privilegios tienen un formato r-xp, 
                # por lo que se emplea una expresion regular para obtnerlos:
                privilegios = re.search('[-rsxpw]{4}', line).group()
                # El mapeo de la direccion de memoria tiene un formato:
                # /bin.. 
                # [stack], [heap], ...
                mapeo = re.search('(/|\[).*', line)
                # Si la direccion no tiene un mapeo, se establece como vacío, 
                # de lo contrario se asgina el encontrado
                mapeo = mapeo.group() if mapeo else "- Vacío -"
                uso = ''
                # Si tiene '/' se trata de Textos o Datos del proceso
                if('/' in mapeo):
                    # Si el proceso tiene permisos de execucion se trata de Texto:
                    if('r-x' in privilegios):
                        # Si la direccion contiene la palabra 'lib' 
                        # se trata de una biblioteca, de lo contrario solo de texto:
                        uso = 'Bib → Texto' if 'lib' in mapeo else 'Texto'
                    # De lo contrario se trata de Datos:
                    else:
                        # Si la direccion contiene la palabra 'lib' 
                        # se trata de una biblioteca, de lo contrario solo de datos:
                        uso = 'Bib → Datos' if 'lib' in mapeo else 'Datos'
                # De lo contrario, se trata de una seccion de:
                # stack, heap , ...
                elif("- Vacío -" not in mapeo):
                    # Se obtiene el nombre de la sección
                    tmp = re.search('\w+', mapeo)
                    if(tmp):
                        # Sí se encontro un nombre, se asigna la primer letra en mayúscuals
                        uso = tmp.group().capitalize()
                # Se anexa el buffer de salido los datos obtenidos:
                buffer.append([uso, pag0, pag1, size, numPag, privilegios, mapeo])
            buffer[-1][1] = buffer[-1][1][4:]
            buffer[-1][2] = buffer[-1][2][4:]
            # Para mostrar de menor a mayor las direcciones de memoria:
            buffer.reverse()
            printBuffer(buffer) # Se muestra el buffer
    except: 
        # En caso de cualquier excepción o finaliza la función
        pass     
    
# Función para mostrar el tamaño en formato de KB, MB o GB, dependiento el tamaño
def convertir(size):
    # Función 
    if(size < 1024):
        return str(size) + 'KB'
    size /= 1024
    if(size < 1024):
        return '{0:.1f}MB'.format(size)
    size /= 1024
    if(size < 1024):
        return '{0:.1f}GB'.format(size)

# Función para imprimir el contenido del buffer:
def printBuffer(buffer):
    for f in buffer:
        message = '{0:12s} {1:9s} - {2:9s} ( {3:6s} , {4:6d} pág. ) {5:4s} {6:s}'.format(
            f[0].rjust(12), f[1], f[2], f[3].rjust(6, ' '), f[4], f[5], f[6])
        # Cada linea se imprime con un color dependiendo del tipo de uso
        if(f[0] == 'Heap' ):
            print_heap(message)
        elif(f[0] == 'Stack'):
            print_stack(message)
        elif(f[0] == 'Texto'):
            print_text(message)
        elif(f[0] == 'Datos'):
            print_datos(message)
        elif(f[0] == ''):
            print_pass(message)
        elif('Bib' not in f[0]):
            print_var(message)
        else: 
            print(message)

def print_heap(message, end = '\n'):
    sys.stderr.write('\x1b[1;31m' + message + '\x1b[0m' + end)

def print_pass(message, end = '\n'):
    sys.stdout.write('\x1b[1;32m' + message + '\x1b[0m' + end)

def print_stack(message, end = '\n'):
    sys.stderr.write('\x1b[1;33m' + message + '\x1b[0m' + end)

def print_var(message, end = '\n'):
    sys.stdout.write('\x1b[1;34m' + message + '\x1b[0m' + end)

def print_text(message, end = '\n'):
    sys.stdout.write('\x1b[1;35m' + message + '\x1b[0m' + end)

def print_datos(message, end = '\n'):
    sys.stdout.write('\x1b[1;36m' + message + '\x1b[0m' + end)

# Mensaje en caso de error de sintaxis:
msg = """
Sintaxis:
jsmap.py PID [PID ...]
"""

if __name__ == '__main__':
    arg = sys.argv
    # Error de sintaxis del comando al no indicar un PID o bandera:
    if(len(arg) < 2):
        print(msg)
        exit(0)
    # Se obtienen todos los PID enviados como argumentos de comandos:
    PID = re.findall('\d+', "-".join(arg))
    # Si no se encontro ningun número(PID):
    if(not PID):
        print("jmap: argument missing")
        exit(0)
    # Para cada PID se genera su MAP
    for pid in PID:
        map(pid)