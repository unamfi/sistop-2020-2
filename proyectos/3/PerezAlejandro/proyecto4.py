# -*- encoding: utf-8
import os
import time
from math import ceil

img = open("fiunamfs.img")			# Leyendo y abriendo archivo. Se declara global para usarlo en otras instancias

name = img.read(8)
img.seek(10)
ver = img.read(3)
img.seek(20)
vol = img.read(15)
img.seek(40)
clu = img.read(5)
img.seek(47)
nuClu = img.read(2)
img.seek(52)
unit = img.read(8)
img.close()

arch = []
size = []
clu1 = []		#Precaucion con el nombre de las variables
aux = []
loc = []
search = 1
flag1 = True
clusterPosition = 2048

def monta():
	img = open("fiunamfs.img")
	'''global arch
	global size
	global clusterPosition
	global loc'''

	while (clusterPosition < 64):
		img.seek(clusterPosition)
		B = img.read(15)
		if(B != 'Xx.xXx.xXx.xXx.'):
			arch.append(B.replace("-","*"))
			img.seek(clusterPosition + 16)
			size.append(int(img.read(8)))
			img.seek(clusterPosition + 25)
			loc.append(int(img.read(5)))
		clusterPosition += 64
	clusterPosition = 64
	img.close()

def sysInfo():
	global name
	global ver
	global vol
	global clu
	global nuClu
	global unit

	print("System Name: " + name)
	print("Version: " + ver)
	print("Volume name: " + vol)
	print("Cluster Bytes: " + clu + " B")
	print("Cluster size directory: " + nuClu + " clusters")
	print("Full size cluster: " + unit)

def delete(file):
	global clusterPosition
	global arch
	global size
	local = []

	with open("fiunamfs.img", "r+") as img:
		img.seek(clusterPosition)
		while(clusterPosition < 64):
			fileName = img.read(15)
			sfileName = fileName.strip()
			if(sfileName == file):
				img.seek(clusterPosition)
				img.write("nul")
				img.write('0'*49)
				print("Deleted file.\n")

				delet = len(arch)
				for i in range(delet):
					arch.pop(0)
					size.pop(0)
				monta()
				break
			else:
				clusterPosition += 64
				img.seek(clusterPosition)
				if(clusterPosition == 64):
					print("NULL\n")

def toPC(path, n):
	global clusterPosition
	global clu1
	global aux
	global search
	global flag1
	pos = 0
	on = 0

	try:
		new = open(path, "r+")
		img = open("fiunamfs.img", "r+")
		img.seek(clusterPosition)
		flag = False
		size = stat(path).st_size

		while(flag == False):
			name = img.read(15)
			if(name == 'Xx.xXx.xXx.xXx.'):
				img.seek(img.tell()-15)
				img.write(n)
				on = file.tell()
				print("File copied")
				flag = True
			img.seek(img.tell()+49)
		img.close()
		img = open("fiunamfs.img", "r+")

		for i in range(len(clu1)):
			c = clu1[i]
			aux.append(int(c[0]))
		print(aux)
		while flag:
			if search in aux:
				search = search + 1
			else:
				flag = False
		return search

		index = clusterPosition*search
		tam = size
		return tam
		img.seek(index)
		img.write(new.read(tam))
		img.close()
		img = open("fiunamfs.img", "r+")
		img.seek(on)
		img.write(srt(search))
		img.close()
	except:
		print("No file")

def toSys(path):
	global loc
	global size
	global clusterPosition

	img = open("fiunamfs.img", "r+")
	w = os.path.getsize(path)
	t = datetime.datetime.strptime(time.ctime(os.path.getctime(path)), "%a %b %d %H:%M:%S %Y")
	crea = str(t.year) + str(t.month).zfill(2) + str(t.hour).zfill(2) + str(t.minute).zfill(2) + str(t.second).zfill(2)
	fm = datetime.datetime.now()
	mod = str(t.year) + str(t.month).zfill(2) + str(t.hour).zfill(2) + str(t.minute).zfill(2) + str(t.second).zfill(2)
	x = loc.index(max(loc))

	origen = loc[x]
	clusterS = math.ceil(size[x]/2048)
	G = (origen + clusterS)*2048
	patch = open(path, "r+")
	d = patch.read(w)

	img.seek(G)
	img.write(d)
	img.close()

	name = path
	img = open("fiunamfs.img", "r+")

	while clusterPosition < 64:
		img.seek(clusterPosition)
		B = img.read(15)
		if B == 'Xx.xXx.xXx.xXx.':
			img.seek(clusterPosition)

			img.write(name)
			img.seek(clusterPosition + 16)

			img.write(srt(w))
			img.seek(clusterPosition + 25)

			img.write(srt(G))
			img.seek(clusterPosition + 31)

			img.write(mod)
			img.seek(clusterPosition + 46)

			img.write(crea)
			img.close()
			patch.close()
			print("Copied file")
		clusterPosition += 64
	clusterPosition = 1024

def menu():
	global name
	global ver
	global vol
	global clu
	global nuClu
	global unit
	global img
	global clusterPosition, arch, size, loc

	sys = True

	if(name == "FiUnamFS" and ver == "0.9"):
		while(sys):
			os.system("clear")
			print("\tFI UNAM File System")
			print("\t1. List files")
			print("\t2. Copy a file")
			print("\t3. Copy a file into system")
			print("\t4. Delete a file")
			print("\t5. File system information")
			print("\t6. Unmount/exit")
			op = input("\t>> ")

			'''-----------------------opciones-----------------------'''
			if (op == 1):
				os.system("clear")
				l = len(arch)
				for i in range(l):
					arch.pop(0)
					size.pop(0)
					loc.pop(0)
				monta()
				for i in range(len(arch)):
					print(arch[i])
				l = len(arch)
				for i in range(l):
					arch.pop(0)
					size.pop(0)
					loc.pop(0)
				monta()
			elif (op == 2):
				os.system("clear")
				file = input("File name>> ")
				toPC((file))
			elif (op == 3):
				os.system("clear")
				path = input("File name>> ")
				toPC((path))
			elif (op == 4):
				os.system("clear")
				path = input("File name>> ")
				delete((path))
			elif (op == 5):
				os.system("clear")
				print("Name: " + name)
				print("Version: " + ver)
				print("Volume: " + vol)
				print("Cluster Size: " + clu + " B")
				print("Number of directory clusters size: " + nuClu)
				print("Unit full size: " + unit)
				print("\n\n(Size on Bytes)")
			elif (op == 6):
				os.system("clear")
				print("Unmounting system...")
				time.sleep(3)
				print("Se ha desmontado el sistema.")
				time.sleep(2.5)
				exit()
	else:
		print("No existe o no es correcto el sistema de archivos.")
		print("Por favor verifica la version, el nombre y/o que exista el sistema")
		exit()

menu()