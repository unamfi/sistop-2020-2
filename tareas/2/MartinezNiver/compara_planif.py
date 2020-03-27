from random import Random
from random import randint
''' Genera los tiempos de llegada de cada proceso de
	de manera aleatoria para un número n de procesos.
''' 
def init_arrives(n):
	count = 0
	arrives = [0]*n
	arrives[0]=0
	for i in range(1,n):
		count = count + randint(1,5)
		arrives[i]= count
	return arrives

''' Genera los tiempos que requiere cada proceso para
	terminar su ejecución de de manera aleatoria para 
	un número n de procesos.
'''
def generator_time(n):
	times = [0]*n
	for i in range(0,n):
		times[i]=randint(1,8)
	return times

'''
	Genera un diccionario que contiene como llaves el 
	nombre del proceso y como valores una lista con
	los tiempos de llegada y de ejecución.
'''
def times_process(names,n):
	arrives = init_arrives(n)
	times = generator_time(n)
	time_dup = [0]*n
	processes = {}
	for i in range(0,len(names)):
		time_dup[i] = [arrives[i],times[i]]
		processes[names[i]] = time_dup[i]
	return processes

'''
	Nos ayuda a realizar la división elemento por
	elemento de dos listas.
'''
def divide_lists(list1,list2):
	list3=[]
	for i in range(0,len(list1)):
		list3.append(list1[i]/list2[i])
	return list3

'''
	Reliza el promedio (media aritmética) de todos
	 los elementos de una lista.
'''
def average(list1):
	x = sum(list1)/len(list1)
	return x

#implmentación de FCFS
def fcfs(processes, n):
	count = 0
	T = 0
	E = 0
	time_list = [0]
	wait_list = [0]
	time_auxs = []
	for i in processes:
		name = i
		times = processes[i]
		a = times[0]
		t = times[1]
		time_auxs.append(t)
		count = count + t
		if a == 0:
			T = a + t
			E = 0
			time_list[0]=T
			wait_list[0]=E
		else:
			T = abs(count - a)
			E = abs(T - t)
			time_list.append(T)
			wait_list.append(E)
	T_tot = average(time_list)
	E_tot = average(wait_list)
	P_list = divide_lists(time_list,time_auxs)
	P_tot = average(P_list)
	print("\nTiempo total: "+ str(count))

	print("\n"+"FCFS:" 	+" T: "+("%.2f" %T_tot)
						+" E: "+("%.2f" %E_tot)
						+" P: "+("%.2f" %P_tot))
	for i in processes:
		name = i
		arrive = processes[i]
		a = arrive[0]
		t = arrive[1]
		for j in range(0,t):
			print (i, end='')


def round_robin(processes, n, q):
	p = []
	time_auxs = []
	arrive_auxs = []
	sec = []
	T_times = [0]*n
	wait_times = [0]*n
	for i in processes:
		name = i
		times = processes[i]
		time_auxs.append(times[1])
		arrive_auxs.append(times[0])
	for i in range(n):
		p.append([])
		p[i]=[1]*time_auxs[i]
		for j in range(0,sum(time_auxs),q):
			if len(p[i]) != 0:
				T_times[i] = T_times[i] + p[i].pop() + j + 1
				sec.append('N')
			else:
				pass
		T_times[i] = abs(time_auxs[i] + arrive_auxs[i]-q)
		wait_times[i] = abs(T_times[i] + time_auxs[i])
	y = q/(q+2)
	E_tot = average(T_times)
	T_tot = average(wait_times) 
	P_list = divide_lists(T_times,wait_times)
	if q == 1:
		P_tot = average(P_list) + q
	else:
		P_tot = average(P_list) + y
	print("\n"+"RR1:" 	+" T: "+("%.2f" %T_tot)
						+" E: "+("%.2f" %E_tot)
						+" P: "+("%.2f" %P_tot))
	for j in sec:
		print (j, end='')

def spn():

	T_tot = 0
	E_tot = 0
	P_tot = 0
	print("\n"+"SPN:" 	+" T: "+("%.2f" %T_tot)
						+" E: "+("%.2f" %E_tot)
						+" P: "+("%.2f" %P_tot))

'''
	A contunuación tenemos el formato que se eligió 
	para representar los parámetros de entrada de cada
	algoritmo. Ya que esto fue implementado mediante un 
	diccionario, tenemos que: las llaves, son el nombre 
	del proceso, mientras que los valores, son listas 
	con dos elementos, el primer índice es el tiempo de 
	llegada del proceso, mientras que el segundo elemento 
	de la lista es el tiempo que requiere el proceso para 
	completar su ejecución.
'''

# n : número de procesos
# m : número de rondas
#names : nombre de proceso
def main():
	n = 5
	m = 1
	names = ['A','B','C','D','E']
	for i in range(0,m):
		processes = times_process(names,n)
		# N : name process
		# A : time arrive
		# t : time execution
		print("\n"+">>>Ronda "+ str(i+1) +"\n")
		print("N " + " A " + " t |"+"N " + " A " 
			+ " t |"+"N " + " A " + " t |"+"N " 
			+ " A " + " t |"+"N " + " A " + " t |")
		print("----------------------------------------------")
		for x, y in processes.items():
			print(x,y,end=' ')

		fcfs(processes, n)
		round_robin(processes, n, 1)
		round_robin(processes, n, 4)
		spn()
main()