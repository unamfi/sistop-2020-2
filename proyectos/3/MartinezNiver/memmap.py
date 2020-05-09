import sys
import os

def file_open(pid):
	path_maps = "/proc/" + str(pid) + "/maps"
	path_smaps = "/proc/" + str(pid) + "/smaps"
	file_maps = open(path_maps,"r")
	file_smaps = open(path_smaps,"r")
	return file_maps, file_smaps

def crop_line(line):
		if len(line) == 6 or len(line) == 7:
			if line[0] != '':
				adress = line[0]
			else:
				adress = ''
			if line[1]	!= '':
				perm = line [1]
			else:
				perm = ''
			if line[4] != '':
				idp = line [4]
			else:
				idp = ''
			if line[5] != '':
				path = line [5]
			else:
				path = ''
		if len(line) == 5:
			if line[0] != '':
				adress = line[0]
			else:
				adress = ''
			if line[1]	!= '':
				perm = line [1]
			else:
				perm = ''
			if line[4] != ' ':
				idp = line [4]
				path = 'None'
		if len(line) <5:
			adress = 0
		return ['QES?',adress,perm,'t',idp,path]

def mesure_page(section):
	if section[1] is not None:
		distance = section[1].split('-')
		begin = int(distance[0],16)
		end = int(distance[1],16)
	else:
		pass		
	return end - begin

def mesure_units(size):
	power = 10**6
	n = 0
	power_labels = {0 : 'k', 1: 'M', 2: 'G', 3: 'T'}
	while size > power:
		size //= power
		n += 1
	return str(round(size,1)) + str(power_labels[n]+'B')

def debug_file(f, s):
	f_temp = open('temp.txt','w')
	count = 0
	for line in reversed(open(f.name).readlines()):
		count += 1
		s = line.rstrip()
		t = s.split()
		v = crop_line(t)
		cad = ' '.join(v)
		f_temp.write(cad+"\n")
	return f_temp.name

def asignament_dir(perm):
	if perm == 'rw--' or perm == 'rw-p':
		return 'BibData'
	if perm == 'r--p' or perm == 'r--p':
		return 'BibTexto'

def do_stuff_with_two_lines(previous_line, current_line,page):
	p = previous_line.split()
	c = current_line.split()
	a = p[page].split('-')
	b = c[page].split('-')
	p1 = a[0]
	p2 = a[1]
	c1 = b[0]
	c2 = b[1]
	if p[4] == c[4] and p[5] == c[5]:
		#list=[p[0],p[4],c[0],c[4],True]
		begin = p1
		end = c2
		l = []
		l.append(begin)
		l.append(end)
		x = l[0]
		y = l[len(l)-1]
		pag = int(y,16) - int(x,16)
		if pag == 1:
			tam = '4KB'
		else:
			aux = pag*4000
			tam = mesure_units(abs(aux))
		return [asignament_dir(p[2]),x,y,tam,abs(pag),p[2],p[5]]
	else:
		#list=[p[0],p[4],c[0],c[4],False]
		begin = p1
		end = p2
		l = [begin, end]
		x = l[0]
		y = l[1]
		pag = int(y,16) - int(x,16)
		if pag == 1:
			tam = '4KB'
		else:
			aux = pag*4000
			tam = mesure_units(abs(aux))
		return [asignament_dir(p[2]),x,y,tam,abs(pag),p[2],'None']

def control_lines(my_f):
	my_file = open(my_f, 'r')
	if my_file:
		 current_line = my_file.readline()
	n=0
	for line in my_file:
		 n += 1
		 previous_line = current_line
		 current_line = line

		 pages = do_stuff_with_two_lines(previous_line, current_line,1)
		 #print(len(pages))
		 color_column(pages,n)
		 
		
def color_column(data,n):
	a = "\033[1;31;46m"+ str(data[0])
	b = "\033[1;30;46m"+ str(data[1]) +'-'+str(data[2])
	c = "\033[1;31;46m"+ str(data[3])
	d = "\033[1;31;46m"+ str(data[4])
	e = "\033[1;31;46m"+ str(data[5])
	f = "\033[1;31;46m"+ str(data[6])
	sec = "\033[1;36;46m SECCION:  "
	tam = "\033[1;36;46m TAMAÑO: "
	per = "\033[1;33;46m PERMISOS: "
	mape = "\033[1;33;46m MAPEO: "
	pag = "\033[1;33;46m PAGINAS:  "
	fle = "\033[1;36;46m <- "
	tam_linea = len(a) + len(b) + len(c) + len (sec) + len(tam) +len(fle)
	linea = '-'*(tam_linea//2+20)
	linead = '_'*(tam_linea//2+16)
	
	print("\033[1;32;46m"+"SECCION"+str(n))
	print("\033[1;32;46m"+linead)
	print(sec,b,tam,c,fle,a)
	print("\033[1;32;46m"+linea)
	print(per,e,mape,f)
	print(pag,d)
	print("\033[1;32;46m"+linead)
	print("\033[1;32;40m"+linead)

def main():
	p = sys.argv
	try:
		if len(p)>2:
			print("¡Parámetro inválido!")
		else:
			f1, f2 =  file_open(p[1])
			if os.path.exists("temp.txt"):
				os.remove("temp.txt")
				control_lines(debug_file(f1,f2))
			else:
				pages = control_lines(debug_file(f1,f2))
	except OSError as e:
		print('Excepción: PID inválido')
		print('Parece que \'' + str(p[1]) + '\' no es un PID válido')
		print('Pruebe buscando el PID para su proceso con pidof')
	except IndexError as error:
		print('Excepción: faltan parámetros')
		print('Ingrese el PID')
		print('Pruebe buscando el PID para su proceso con pidof')
main()
