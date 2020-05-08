#!/usr/bin/python3
"""
Para este proyecto se hara un parseo del archivo smaps a travez del cual se obtendran los datos deseados
Para este archivo se sigue una regla del zen de python "explicit is better than implicit" Por lo que las direcciones 
de memoria serán mostradas de forma explicita. 

Entradas: python3 -m" archivoMap -s archivoSmap
        en caso de desear utilizar pid:
        python3 -p pid
"""

# Importamos las Bibliotecas Necesarias
import re
import argparse
import os
from termcolor import cprint, colored  # Hay que instalarla
from functools import reduce

# Definimos funciones utiles
def crear_parser():
    parser = argparse.ArgumentParser(description="""Pato map, un programa que igual y te mapea la memoria como te la rompe.\n
    Se debe utilizar ya sea la opción [-p] o [-m y -s] Ej:
    python3 patomap.py -p 53
    python3 patomap.py -s /proc/34/maps
    python3 patomap.py -s /home/gwolf/Downloads/smapdump""",
    epilog="En caso de bugs reportar a pato@patomail.com",formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-m','--m', dest='map',type=argparse.FileType('r'),
                    help='Ruta del archivo map')
    parser.add_argument('-s','--smap',dest='smap',type=argparse.FileType('r'),
                    help='Ruta del archivo smap')
    parser.add_argument('-p','--pid',dest='pid',type=int,
                    help='Pid del proceso.Se buscará en: /proc/{PID]}/ \n ->Esta opcion hace que se ignoren las demas')
    return parser.parse_args()


def revisar_opciones(args):
    if not (args.map or args.smap or args.pid) :
        print("Utilize al menos una de las opciones:")
        print("Consulte: python3 patomap.py -h")
        exit()
        ###ver que utilize ya sea pid o map y smap.
        ###si utiliza los 3 alv solo pid
        ### Si utiliza map y no smap -> Validar este caso
    elif args.pid:
        base= "/proc/{}".format(args.pid)
        ruta = [base+"/smaps",base+"/maps"]
    elif args.smap and args.maps:
        ruta = [args.smap,args.maps]
    elif args.smap or args.maps:
        print("Debes especificar ambos archivos, smap y maps")
        exit()
    else:
        print("No se que hiciste")
        print(args)
        exit()
    return ruta

def leer_archivo(ubicacion):
    """
    Permite leer el contenido de un archivo dada su ubicacion
    ----
    Regresa
    str => el contenido del archivo
    ----
    puede arrojar
    FileNotFoundError => Si no encuentra el archivo
    PermissionError => SI no tengo permisos para leer el archivo
    """
    archivo = open(ubicacion, 'r')
    texto = archivo.read()
    archivo.close()
    return texto

# obtenemos informacion imporante del archivo
def obtener_info_smaps(texto_smaps):
    """
    A traves del contenido de smaps obtenemos los elementos imporantes de cada segmento
    ---
    Regresa
    list(dict) => lista de segmentos. cada segmento es un diccionario donde se puede acceder mediante su llave al valor que deseamos
    """
    # Por medio de una expresion regular analizamos cada segmento de memoria y obtenemos la informacion importante de cada uno
    expresion_regular = r"([\da-f]+)\-([\da-f]+) (r|-)(w|-)(x|-)(s|p) [\da-f]+ [\da-f]+:[\da-f]+ [\da-f]+ +([\[\]\/\-\.\w]*)\n?Size: +(\d+) ([MkGgKm]B)\n?KernelPageSize: +(\d+) ([MkGgKm]B)\n?MMUPageSize: +(\d+) ([MkGgKm]B)[\n: \w\t]*VmFlags:(( \w*)+)"
    patron = re.compile(expresion_regular)
    s = patron.findall(texto_smaps)
    lista_segmentos = []
    for v in s:
        segmento = dict()
        segmento["inicio"] = v[0]
        segmento["final"] = v[1]
        segmento["leer"] = v[2]
        segmento["escribir"] = v[3]
        segmento["ejecutar"] = v[4]
        segmento["compartido"] = v[5]
        segmento["mapping"] = v[6]
        segmento["Tamano"] =(v[7], v[8])  # (valor, unidad)
        segmento["TamanoMMUPagina"] = (v[9], v[10])  # (valor, unidad)
        segmento["RSS"] = (v[11], v[12])  # (valor, unidad)
        lista_segmentos.append(segmento)
    return lista_segmentos

def convertir(unidad):
    if unidad.upper() == "KB":
        return 1000
    if unidad.upper() == "MB":
        return 1000000
    return 1000000000

def organizar_informacion_unitario(segmento):
    mapeo = segmento["mapping"]
    tamano = segmento["Tamano"][0] + " " + segmento["Tamano"][1]
    num_paginas = str(float(segmento["Tamano"][0]) * convertir(segmento["Tamano"][1]) / (float(segmento["TamanoMMUPagina"][0]) * convertir(segmento["TamanoMMUPagina"][1])))
    de = segmento["inicio"]
    a = segmento["final"]
    permisos = segmento["leer"] + segmento["escribir"] + segmento["ejecutar"]
    uso = "???"
    if mapeo == '[stack]':
        uso = "Stack"
    elif mapeo == '[heap]':
        uso = "Heap"
    elif mapeo == "":
        uso = mapeo = "vacio"
    elif segmento["leer"].lower() == 'r' and segmento["ejecutar"].lower() == "x" and "lib" in mapeo:
        uso = "Bib→Texto"
    elif segmento["leer"].lower() == 'r' and "lib" in mapeo:
        uso = "Bib→Datos"
    elif segmento["leer"].lower() == 'r' and segmento["ejecutar"].lower() == "x" and "/usr/bin" in mapeo:
        uso = "Texto"
    elif segmento["leer"].lower() == 'r' and "/usr/bin" in mapeo:
        uso = "Datos"
    return (uso, de, a, tamano, num_paginas, permisos, mapeo)

def organizar_informacion(lista_segmentos):
    lista_identificados = []
    for segmento in lista_segmentos:
        segmento_identificado = organizar_informacion_unitario(segmento)
        lista_identificados.append(segmento_identificado) 
    return lista_identificados

def imprimir_salida(lista_segmentos):
    def calcula_maximo(lista_segmentos, i, cadena):
        return len(reduce(lambda s1, s2 : s1 if len(s1) >= len(s2) else s2, map(lambda l : l[i], lista_segmentos), cadena))

    def agregar_espacios(cadena, n):
        if n <= len(cadena):
            return cadena
        resta = n - len(cadena) 
        agregar = " " * (resta // 2)
        agregar_final = "" if resta % 2 == 0 else " "
        return agregar + cadena + agregar + agregar_final
    
    nombres = ['USO', 'DE PAG.', 'A PAG.', 'TAMAÑO', 'NUM. PAG.', 'PERMISOS', 'MAPEO']
    colores = ['red', 'green', 'green', 'magenta', 'blue', 'cyan', 'yellow']
    maximos = [calcula_maximo(lista_segmentos, i, cadena) for i, cadena in enumerate(nombres)]
    # Imprimir encabezados
    for nombre, color, maximo in zip(nombres, colores, maximos):
        print(" | ", end ="")
        cprint(agregar_espacios(nombre, maximo), color, 'on_grey', attrs = ['bold'], end = '')
    print()
    for i, segmento in enumerate(lista_segmentos):
        color_fondo = "on_white" if i % 2 == 0 else "on_grey"
        for j, (color, maximo, elemento) in enumerate(zip(colores, maximos, segmento)):
            simbolo = "|" if j != 2 else "-"
            print(" {} ".format(simbolo), end ="")
            cprint(agregar_espacios(elemento, maximo), color, color_fondo, end = '')
        print()

if __name__ == "__main__":
    try:
        # Obtenemos la ubicacion del archivo smaps
        ubicacion_smaps, ubiacion_maps = revisar_opciones(crear_parser())
        # Obtenemos el contenido del archivo smaps
        texto_smaps = leer_archivo(ubicacion_smaps)
        lista_segmentos = obtener_info_smaps(texto_smaps)

        
        # Determinamos a que corresponde cada segmento
        segmentos_organizados = organizar_informacion(lista_segmentos)

        # Mostramos en pantalla
        imprimir_salida(segmentos_organizados)
    except PermissionError as e:  # Si no tenemos permisos para leer un archivo
        print("No tienes permisos para leer ese proceso/archivo :(")
        print(e)
        exit()
    except FileNotFoundError as e:  # Si no encontramos un archivo
        print("No se ha encontrado el archivo")
        print(e)
        exit()
    except Exception as e:  # Cualquier otro error
        print("No tengo permiso para leer ese proceso o no existe.\n\
         Si es un pid, verifique que el proceso este corriendo")
        print(e)
        exit()

          
       