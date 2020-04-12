from threading import Semaphore



vis = True #falso para modo texto, verdadero para modo visual

#Rendevouz para refrescar la pantalla
sigHilos = Semaphore(0)
sigInterfaz = Semaphore(0)

grafico = [""]*8

grafico[0] = "                      "
grafico[1] = "o= ==================o"
grafico[2] = "|       |     |       "
grafico[3] = "|       |     |      |"
grafico[4] = "|                    |"
grafico[5] = "|                    |"
grafico[6] = "o=  =================o"
grafico[7] = ""


