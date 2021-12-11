#!/usr/bin/python3
import mmap
import os.path
import time
import struct

datos=''
archivo = '/tmp/usando_mmap'

# Hoy en día (Python 3), ya no es lo mismo una cadena que un arreglo
# de bytes. Tenemos que codificar nuestras cadenas para poder
# guardarlas directamente (y para saber su longitud real)
def a_bytes(c):
    return c.encode('utf-8')

# La decodificación también tiene que ser expresa.
# Agrego únicamente strip() para eliminar los espacios en blanco...
def de_bytes(c):
    return c.decode('utf-8').strip()

# ¿Existe el archivo en que vamos a trabajar? Si no, lo creamos.
def verifica(archivo):
    if not(os.path.isfile(archivo)):
        fh = open(archivo,'w')
        fh.seek(1048576 * 1048576 - 1)
        fh.write(chr(0))
        fh.close()
    return True

# Reporto y registro el último uso
def ultimo_uso():
    print(de_bytes(datos[0:70]))

    txt = b'El ultimo uso de este archivo fue: '
    datos[0:len(txt)] = txt
    datos[(len(txt)):59] = a_bytes( time.asctime() )

# Algunos datos de este programa... Aprovecho para mostrar de rapidito
# la codificación/decodificación de tipos de dato usando
# struct.pack/unpack
def este_programa():
    name=__file__
    tam=os.stat(name).st_size

    print("\n\nLa vez anterior, este programa se llamaba %s y medía %s"  %
          (de_bytes(datos[100:150]), de_bytes(datos[150:160])))
    print('Este programa se llama %s y mide %s' % (name, tam))
    # Algunos tipos de dato habituales para pack/unpack:
    # ?: boolean
    # h: short
    # l: long
    # i: int
    # f: float
    # q: long long int
    print('En realidad, conviene más leerlo como entero: %d' %
          struct.unpack_from('i', datos[161:165]))

    datos[100:150] = a_bytes( ('%50s' % name) )
    datos[150:160] = a_bytes( ('%10d' % tam) )
    datos[161:165] = struct.pack('i', tam)


# Verificamos y abrimos nuestro archivo "mmapeado"
verifica(archivo)
fh = open(archivo, 'a+')
datos = mmap.mmap(fh.fileno(), 0)

# Y jugamos un poquito con él
ultimo_uso()
este_programa()

time.sleep(60)
