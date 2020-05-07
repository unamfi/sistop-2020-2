#!/usr/bin/python3

import re
import sys
import os

def map(pid):
    try:
        with open('/proc/' + pid + '/maps' , 'r') as file:
            buffer = []
            with open('/proc/' + pid + '/cmdline' , 'r') as f_name:
                name = f_name.readline()
                if(not name):
                    exit(0)
                print(pid + ':\t' + name)
                print('{0:12s} {1:9s} - {2:9s} ( {3:6s} , {4:6s} ) {5:4s} {6:s}'.format(
                    '     Uso'.ljust(12), ' De pág', '  A pág', ' Size', '   Núm Pág ', 'Modo', 'Mapping'))
            for line in file:
                paginas = re.findall('[0-9a-f]+', line)[0:2]
                pag0 = paginas[0][0:-3]
                pag1 = paginas[1][0:-3]
                numPag = int(pag1,16) - int(pag0,16)
                size = convertir(numPag * 4)
                privilegios = re.search('[-rsxpw]{4}', line).group()
                mapeo = re.search('(/|\[).*', line)
                mapeo = mapeo.group() if mapeo else "- Vacío -"
                uso = ''
                if('/' in mapeo):
                    if('r-x' in privilegios):
                        uso = 'Bib → Texto' if 'lib' in mapeo else 'Texto'
                    else:
                        uso = 'Bib → Datos' if 'lib' in mapeo else 'Datos'
                elif("- Vacío -" not in mapeo):
                    tmp = re.search('\w+', mapeo)
                    if(tmp):
                        uso = tmp.group().capitalize()
                buffer.append([uso, pag0, pag1, size, numPag, privilegios, mapeo])
            buffer[-1][1] = buffer[-1][1][4:]
            buffer[-1][2] = buffer[-1][2][4:]
            buffer.reverse()
            printBuffer(buffer) # Se muestra el buffer
    except: 
        pass     
    
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

def printBuffer(buffer):
    for f in buffer:
        message = '{0:12s} {1:9s} - {2:9s} ( {3:6s} , {4:6d} pág. ) {5:4s} {6:s}'.format(
            f[0].rjust(12), f[1], f[2], f[3].rjust(6, ' '), f[4], f[5], f[6])
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

msg = """
Sintaxis:
jsmap.py PID [PID ...]
"""

if __name__ == '__main__':
    arg = sys.argv
    if(len(arg) < 2):
        print(msg)
        exit(0)
    PID = re.findall('\d+', "-".join(arg))
    if(not PID):
        print("jmap: argument missing")
        exit(0)
    for pid in PID:
        map(pid)
