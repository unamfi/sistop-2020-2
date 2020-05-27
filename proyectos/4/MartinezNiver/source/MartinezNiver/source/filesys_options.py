import mmap

def lectura_SB():
	f = open('fiunamfs.img','r+b')
	mapfs = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
	nombre = mapfs[0:8].decode('ascii')
	version = mapfs[10:13].decode('ascii')
	volumen = mapfs[20:35].decode('ascii')
	cluster = int(mapfs[40:45].decode('ascii'))
	num_cluster = int(mapfs[47:49].decode('ascii'))
	tot_cluster = int(mapfs[52:60].decode('ascii'))

	mapfs.close()
	return [nombre,version,volumen,cluster,num_cluster,tot_cluster]

def lectura_entradas(input):
	nombre = entrada[0:15].decode('ascii').strip()
	archivo = entrada[16:24].decode('ascii')
	cluster = entrada[25:30].decode('ascii')
	creacion = entrada[31:45].decode('ascii')
	modificacion = entrada[46:60].decode('ascii')
	num_entrada = -1
	return [nombre,archivo,cluster,creacion,modificacion,num_entrada]

def listar():
	entradas = []
	f = open('fiunamfs.img','a+b')
	mapfs = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
	a = lectura_SB()
	for i in range(64):
		entrada_aux = int(a[3]) + i * 64
		entrada = mapfs[entrada_aux:entrada_aux+64]
		if entrada[0:15].decode('ascii').strip() != 'Xx.xXx.xXx.xXx.':
			entradas.append(entrada)
	print('\tnombre\t','tamaño',' cluster',' fecha crea','\tfecha mod')
	for e in entradas:
		print(e[0:15].decode(),e[16:24].decode(),e[25:30].decode(),e[31:35].decode()+'/'+e[35:37].decode()+'/'+e[37:39].decode(),e[46:50].decode()+'/'+e[50:52].decode()+'/'+e[52:54].decode())

def desfragmentar():
	print('Se desfragmenta así')

def remover(file):
	print('Se eliminar el archivo',file)

def copiar_sistArchivos(file):
	print('El archivos que se copiará',file)