#Rene Vazquez Peñaloza
#Sistemas Operativos
#El Problema de Santa

import threading 
import time
import random 

SantaSem = threading.Semaphore(0)
RenoSem = threading.Semaphore(0)
ElfoAyudaSem = threading.Semaphore(3)
ElfoSem = threading.Semaphore(0)

RenosContador = 0 
ren = 0 
ElfosContador = 0
elfs = 0
turn = 1

Renos = 9
Elfos = 9
ElfosAyuda = 3
TO_WAKE_UP = 7
TO_HELP = 2

RenosID = ["A","B","C","D","F","G","H","I","J"]
ElfoID = ["1","2","3","4","5","6","7","8","9"]

def santa():
	global RenosContador
	global elfs
	global turn
	print ("Estoy cansado")
	print ("Dormir")
	for i in range(TO_WAKE_UP):
        SantaSem.acquire()
        print ("Santa despierto")
	    if elfs == ElfosAyuda:
            elfs = 0
            print ("Cual es el problema")
            for i in range(ElfosAyuda:
                print ("Santa ha ayudado {} de 3 elfos". format(i+1))
                ElfoAyudaSem.release()
            print ("Santa termino {}".format(turn))
            turn += 1
            for i in range(ElfosAyuda):
                ElfoSem.release()
        elif RenosContador == Renos:
                RenosContador = 0
                preparesleight()
                for i in range(Renos):
                    RenoSem.release()
				
def reindeer():
	global RenosContador
	global ren
	
	num = RenosContador
	RenosContador += 1
	print ("  {} aqui").format(RenosID[num]))
    time.sleep(random,randint(5,7))

    ren += 1
    if ren == 9:
        print ("   Renos {} yo soy {}").format(RenosID[num], ren))
		SantaSem.release()
    else:
        print ("   Renos {} llegando").format(RenosID[num]))

    RenoSem.acquire()
        print ("   {} listos ").format(RenosID[num]))
        print ("   Renos {} terminaron").format(RenosID[num]))

def elf():

	global ElfosContador
	global elfs
	
	num = ElfosContador
    ElfosContador += 1 
    print ("Hola !! {}").format(ElfoID[num]))

    for i in range(TO_HELP)
		time.sleep(random,randint(1,5))
		ElfoAyudaSem.acquire()
		elf = elfs + 1
		elfs += 1
		if elf < 3:
			print (" {} Yo tengo una pregunta {} espera".format(ElfoID[num], elf))
		elif elf == ElfosAyuda:
			print (" {} Yo tengo una pregunta {} Santa".format(ElfoID[num], elf))
			SantaSem.release()
		ElfoSem.acquire()
		print ("{} recibiendo ayuda".format(ElfoID[num]))
	print (" {} termino".format(ElfoID[num]))


def preparesleight():
    print ("Santa dice: juguetes listos")
    print ("Santa carga los juguetes")
    print ("Santa dice: hasta las siguientes vacaciones")
    print ("Santa dice: vamos a dormir")

def main()

threads = []
s = threading.Thread(target=santa)
threads.append(s)

for i in range(Elfos):
    e = threading.Thread(target=elf)
threads.append(e)

for i in range(Reindeer):
    r = threading.Thread(target=reindeer)
threads.append(r)

for t in threads:
    t.start()

for t in threads:
    t.join()

print ("Fin de las vacaciones")

if __name__ "__main__":
    main ()