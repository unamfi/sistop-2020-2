# *-* encoding: utf-8 *-*
#!/usr/bin/python
import threading
import subprocess
import os, sys
import time

os.system("clear")

print("\t\nIntroduce el proceso")
opt = input("\t\n>> ")		#Se introduce el PID

proc = subprocess.getoutput("pmap $$ " + opt) 	#Se obtiene el 'PMAP'
dash = subprocess.getoutput("pmap $$ | grep \"dash\"")
bash = subprocess.getoutput("pmap $$ | grep \"bash\"")
pila = subprocess.getoutput("pmap $$ | grep \"pila\"")
anon = subprocess.getoutput("pmap $$ | grep \"anon\"")
lib = subprocess.getoutput("pmap $$ | grep \"lib\"")
ld = subprocess.getoutput("pmap $$ | grep \"ld\"")

os.system("clear")
print("\t\tPMAP\n\n")
print(proc)

time.sleep(5)	#Tiempo a esperar a que se muestre la siguiente sección

os.system("clear")
print("\t\tPMAP: dash\n\n")
print(dash)
print("Si se puede leer esto, no hay nada que mostrar.")

time.sleep(5)

os.system("clear")
print("\t\tPMAP: bash\n\n")
print(bash)
print("Si se puede leer esto, no hay nada que mostrar.")

time.sleep(5)

os.system("clear")
print("\t\tPMAP: pila")
print(pila)
print("Si se puede leer esto, no hay nada que mostrar.")

time.sleep(5)

os.system("clear")
print("\t\tPMAP: anon")
print(anon)
print("Si se puede leer esto, no hay nada que mostrar.")