import sys
import filesys_options as fo

def main():
	adv = ' > Revise sus entradas o ingrese \'?\' para ayuda'
	head = '\n\tcomando\tarchivo\truta\tacción\tdescripción'
	lis = '\n\tls\tnone\tnone\tlistar\tLista los archivos de sistema se archivos'
	des = '\n\tdg\tnone\tnone\tdesfrag\tDefragmenta FiunamFS'
	rem = '\n\trm\t<name>\tnone\tremover\tRemueve un archivo de FiunamFS'
	cpf = '\n\tcpfs\t<name>\tnone\tcopiar\tCopia de FiunamFS hacia la PC'
	cppc = '\n\tcppc\t<name>\t<path>\tcopiar\tCopia de la PC hacia el FiunamFS'

	try:
		op = sys.argv[1]
		l_args = len(sys.argv)
		if l_args == 2:
			if op == '?':
				print(head,lis,des,rem,cpf,cppc)
			elif op == 'ls':
				fo.listar()
			elif op == 'dg':
				fo.desfragmentar()
			else:
				print(adv)
		elif l_args == 3:
			if op == 'rm':
				fo.remover(sys.argv[2])
			elif op == 'cpfs':
				fo.copiar_sistArchivos(sys.argv[2])
			elif op == 'cppc':
				print('Copiar a la PC')
			else:
				print(adv)
		else:
			print(adv)
	except:
		print('Faltan parámetros','\n',adv)
main()