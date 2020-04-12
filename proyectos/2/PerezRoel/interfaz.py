import curses
from time import sleep
import proyecto2 as pyt2
import config as c
from threading import Semaphore, Thread


def menu():
	scr = curses.initscr()
	curses.noecho()
	dims = scr.getmaxyx() #dimension de la consola

	q = -1
	while q != 113 and q != 81:

		scr.addstr(1,dims[1]-24, 'Presione \'q\' para salir')

		scr.nodelay(1)
		q = scr.getch()

		scr.addstr(2,(dims[1]-39)//2,' _____ _   _            __            ') #y,x,texto
		scr.addstr(3,(dims[1]-39)//2,'|  ___| | | |          / _|           ')
		scr.addstr(4,(dims[1]-39)//2,'| |__ | | | |__  _   _| |_ ___  _ __  ')
		scr.addstr(5,(dims[1]-39)//2,'|  __|| | | \'_ \\| | | |  _/ _ \\| \'_ \\ ')
		scr.addstr(6,(dims[1]-39)//2,'| |___| | | |_) | |_| | || (_) | | | |')
		scr.addstr(7,(dims[1]-39)//2,'\\____/|_| |_.__/ \\__,_|_| \\___/|_| |_|')

		scr.addstr(8,(dims[1]-50)//2,'                   _   _                         \n')
		scr.addstr(9,(dims[1]-50)//2,'                  | | | |                        \n')
		scr.addstr(10,(dims[1]-50)//2,'  ___ _ __     ___| | | |_ _ __ ___  _ __   ___  \n')
		scr.addstr(11,(dims[1]-50)//2,' / _ \\ \'_ \\   / _ \\ | | __| \'__/ _ \\| \'_ \\ / _ \\ \n')
		scr.addstr(12,(dims[1]-50)//2,'|  __/ | | | |  __/ | | |_| | | (_) | | | | (_) |\n')
		scr.addstr(13,(dims[1]-50)//2,' \\___|_| |_|  \\___|_|  \\__|_|  \\___/|_| |_|\\___/ \n')

		scr.addstr(16,(dims[1]//2)-15,'1. El problema')
		scr.addstr(18,(dims[1]//2)-15,'2. Ejecución visual')
		#scr.addstr(20,(dims[1]//2)-15,'3. Ejecución en texto')

		#scr.nodelay(0)
		
		s = -1

		if q == 49:
			scr.clear()
			scr.nodelay(1)
			while s != 115 and s != 83:
				scr.addstr(1, dims[1]-33,'Presiona \'s\' parar salir al menú')
				scr.addstr(2, (dims[1]-20)//2,'El bufón en el trono')
				scr.addstr(3, 2,'El bufón de la corte tiene un pasatiempo secreto: le gusta disfrazarse del rey y sentarse en el trono. Sin embargo, solo puede hacer esto cuando no hay nadie presente en la sala: ni el rey ni los cortesanos. El bufón aprovechará cualquier oportunidad que tenga para darse este lujo. El rey suele ausentarse por periodos considerables de tiempo, mientras que varios cortesanos pueden entrar y salir de la sala. Si el rey llega mientras el bufón está sentado, el bufón tiene que levantarse inmediatamente y cederle el trono. Si un cortesano llega mientras el bufón está sentado, pensará que es el rey y no lo molestará. El bufón también es impaciente, por lo que si cuenta que ya pasaron N cortesanos por la sala y no lo han dejado a solas con el trono, aún en presencia del rey, cerrará maliciosamente la puerta de los cortesanos y esperará a que todos se vayan. Los cortesanos tendrán que esperar afuera. Desafortunadamente, cuando hay M cortesanos esperando, éstos se ponen ruidosos, y el bufón tiene abrirles la puerta, aún si no está sentado. En ocasiones, el bufón es lo suficientemente rápido para abrirles la puerta y sentarse en el trono antes de que entren. ')

				scr.nodelay(0)
				s = scr.getch()
				scr.clear()

		elif q == 50:
			scr.clear()
			scr.nodelay(1)

			hiloRey = Thread(target = pyt2.rey, args = [])
			hiloBufon = Thread(target = pyt2.bufon, args = [])
			hiloCortesanos = Thread(target = pyt2.llegadaCortesanos, args = [])

			hiloRey.start()
			hiloBufon.start()
			hiloCortesanos.start()

			while s != 115 and s != 83:
				s = scr.getch()

				scr.addstr(1,(dims[1]-20)//2,"El bufón en el trono") #y,x,texto
				c.sigHilos.acquire()
				scr.clear()
				scr.addstr(4,(dims[1]-23)//2,c.grafico[0]) #y,x,texto
				scr.addstr(5,(dims[1]-23)//2,c.grafico[1]) #y,x,texto
				scr.addstr(6,(dims[1]-23)//2,c.grafico[2]) #y,x,texto
				scr.addstr(7,(dims[1]-23)//2,c.grafico[3]) #y,x,texto
				scr.addstr(8,(dims[1]-23)//2,c.grafico[4]) #y,x,texto
				scr.addstr(9,(dims[1]-23)//2,c.grafico[5]) #y,x,texto
				scr.addstr(10,(dims[1]-23)//2,c.grafico[6]) #y,x,texto
				scr.addstr(12,(dims[1]-66)//2,c.grafico[7]) #y,x,texto
				scr.refresh()
				sleep(0.25)
				c.sigInterfaz.release()


		elif q == 51:
			scr.clear()
			scr.nodelay(1)
			#while s != 115 and s != 83:


		sleep(0.05)

	#scr.getch()
	curses.endwin()



menu()