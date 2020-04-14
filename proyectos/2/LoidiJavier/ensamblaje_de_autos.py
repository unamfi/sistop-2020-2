from threading import Semaphore, Thread, Lock

numero_de_autos=0

cuenta_motor = 0  #cuentas de elementos independientes
cuenta_seccion_de_chasis = 0
cuenta_seccion_de_transmision = 0
cuenta_llantas = 0
cuenta_pinturas = 0

cuenta_motor_chasis = 0  #cuentas de elementos compuestos
cuenta_transmision_llantas = 0
cuenta_autos_sin_pintura = 0
cuenta_autos = 0

total_motor = 0  #totales de elementos independientes
total_seccion_de_chasis = 0
total_seccion_de_transmision = 0
total_llantas = 0
total_pinturas = 0

total_motor_chasis = 0  #totales de elementos compuestos
total_transmision_llantas = 0
total_autos_sin_pintura = 0
total_autos = 0

mutex_print = Semaphore(1) #mutex para imprimir correctamente

mutex_motor = Semaphore(1) #mutexes de elementos independientes
mutex_seccion_de_chasis = Semaphore(1)
mutex_seccion_de_transmision = Semaphore(1)
mutex_llantas = Semaphore(1)
mutex_pinturas = Semaphore(1)

mutex_motor_chasis = Semaphore(1) #mutexes de elementos compuestos
mutex_transmision_llantas = Semaphore(1)
mutex_autos_sin_pintura = Semaphore(1)
mutex_autos = Semaphore(1)

hay_motor = Semaphore(0)  #barreras de elementos independientes
hay_seccion_de_chasis = Semaphore(0)
hay_seccion_de_transmision = Semaphore(0)
hay_llantas = Semaphore(0)
hay_pintura = Semaphore(0)

hay_motor_chasis = Semaphore(0)  #barreras de elementos compuestos
hay_transmision_llantas = Semaphore(0)
hay_auto_sin_pintura = Semaphore(0)

mutex_completado = Semaphore(0)  #barrera de finalizacion


#LAS FUNCIONES A CONTINUACION SON SIMILARES POR LO QUE SOLO COMENTARE LAS SECCIONES PERTINENTES UNA SOLA VEZ


def constructor_motor(): 
    global mutex_motor, cuenta_motor, total_motor, mutex_print, hay_motor

    mutex_motor.acquire()  #se protege las variables de cuenta y totales

    cuenta_motor = cuenta_motor + 1
    total_motor = total_motor + 1

    mutex_print.acquire()
    print("\n Se construyó el motor numero",total_motor) 
    mutex_print.release()

    mutex_motor.release()

    hay_motor.release()  #se hace una señalización de que hay motor disponible


def constructor_seccion_de_chasis():
    global mutex_seccion_de_chasis, cuenta_seccion_de_chasis, total_seccion_de_chasis, hay_seccion_de_chasis, mutex_print

    mutex_seccion_de_chasis.acquire()

    cuenta_seccion_de_chasis = cuenta_seccion_de_chasis + 1
    total_seccion_de_chasis = total_seccion_de_chasis + 1

    mutex_print.acquire()
    print("\n Se construyó la seccion de chasis numero",total_seccion_de_chasis)
    mutex_print.release()

    if(cuenta_seccion_de_chasis > 1):
        hay_seccion_de_chasis.release()  #aqui tambien se hace una señalización pero con una condicional, por lo que seria un torniquete

    mutex_seccion_de_chasis.release()


def constructor_seccion_de_transmision():
    global mutex_seccion_de_transmision, cuenta_seccion_de_transmision, total_seccion_de_transmision, hay_seccion_de_transmision, mutex_print

    mutex_seccion_de_transmision.acquire()

    cuenta_seccion_de_transmision = cuenta_seccion_de_transmision + 1
    total_seccion_de_transmision = total_seccion_de_transmision + 1

    mutex_print.acquire()
    print("\n Se construyó la seccion de transmision numero",total_seccion_de_transmision)
    mutex_print.release()

    if(cuenta_seccion_de_transmision > 3):
        hay_seccion_de_transmision.release()

    mutex_seccion_de_transmision.release()


def constructor_llantas():
    global mutex_llantas, cuenta_llantas, total_llantas, mutex_print, hay_llantas

    mutex_llantas.acquire()

    cuenta_llantas = cuenta_llantas + 1
    total_llantas = total_llantas + 1

    mutex_print.acquire()
    print("\n Se construyó la llanta numero",total_llantas)
    mutex_print.release()

    if(cuenta_llantas > 3):
        hay_llantas.release()

    mutex_llantas.release()


def mezclador_pintura():
    global mutex_pinturas, cuenta_pinturas, total_pinturas, mutex_print, hay_pintura

    mutex_pinturas.acquire()

    cuenta_pinturas = cuenta_pinturas + 1
    total_pinturas = total_pinturas + 1

    mutex_print.acquire()
    print("\n Se mezclo la pintura numero",total_pinturas)
    mutex_print.release()

    mutex_pinturas.release()

    hay_pintura.release()


def ensamblar_motor_con_seccion_de_chasis():
    global hay_motor, hay_seccion_de_chasis, cuenta_motor, cuenta_seccion_de_chasis, total_motor_chasis, mutex_motor_chasis, mutex_motor, mutex_seccion_de_chasis, cuenta_motor_chasis, mutex_print, hay_motor_chasis

    hay_motor.acquire()
    hay_seccion_de_chasis.acquire()   #debe esperar a una señalizacion de sus elementos independientes de que estan listos

    mutex_motor_chasis.acquire()   #tambien se debe proteger las variables que cuentan a este elemento compuesto

    total_motor_chasis = total_motor_chasis + 1

    mutex_motor.acquire()
    mutex_seccion_de_chasis.acquire()

    mutex_print.acquire()
    print("\n ---> Hay",cuenta_motor,"motor/es y",cuenta_seccion_de_chasis,"secciones de chasis.")   
    print("\n ---> Se ensamblo 1 motor con 2 secciones de chasis. Se ensamblo el motor-chasis numero",total_motor_chasis)
    mutex_print.release()

    cuenta_motor = cuenta_motor - 1
    cuenta_seccion_de_chasis = cuenta_seccion_de_chasis - 2   #se decrementan los valores de los elementos independientes no sin antes haberlos protegido

    cuenta_motor_chasis = cuenta_motor_chasis + 1   #se aumenta la cuenta del elemento compuesto

    mutex_seccion_de_chasis.release()
    mutex_motor.release()

    hay_motor_chasis.release()

    mutex_motor_chasis.release()


def ensamblar_transmision_con_llantas():
    global hay_seccion_de_transmision, hay_llantas, cuenta_seccion_de_transmision, cuenta_llantas, total_transmision_llantas, mutex_transmision_llantas, mutex_seccion_de_transmision, mutex_llantas, cuenta_transmision_llantas, mutex_print, hay_transmision_llantas

    hay_seccion_de_transmision.acquire()
    hay_llantas.acquire()

    mutex_transmision_llantas.acquire()

    total_transmision_llantas = total_transmision_llantas + 1

    mutex_seccion_de_transmision.acquire()
    mutex_llantas.acquire()

    mutex_print.acquire()
    print("\n ---> Hay",cuenta_seccion_de_transmision,"secciones de transmision y",cuenta_llantas,"llantas.")
    print("\n ---> Se ensamblo 4 secciones de transmision con 4 llantas. Se ensamblo el transmision-llantas numero",total_transmision_llantas)
    mutex_print.release()

    cuenta_seccion_de_transmision = cuenta_seccion_de_transmision - 4
    cuenta_llantas = cuenta_llantas - 4

    cuenta_transmision_llantas = cuenta_transmision_llantas + 1

    mutex_llantas.release()
    mutex_seccion_de_transmision.release()

    hay_transmision_llantas.release()

    mutex_transmision_llantas.release()


def ensamblar_auto():
    global hay_motor_chasis, hay_transmision_llantas, cuenta_autos_sin_pintura, total_autos_sin_pintura, cuenta_motor_chasis, cuenta_transmision_llantas, mutex_autos_sin_pintura, mutex_motor_chasis, mutex_transmision_llantas, mutex_print, hay_auto_sin_pintura

    hay_motor_chasis.acquire()
    hay_transmision_llantas.acquire()

    mutex_autos_sin_pintura.acquire()

    total_autos_sin_pintura = total_autos_sin_pintura + 1

    mutex_motor_chasis.acquire()
    mutex_transmision_llantas.acquire()

    mutex_print.acquire()
    print("\n ------> Hay",cuenta_motor_chasis,"motor-chasis y",cuenta_transmision_llantas,"transmision-llantas.")
    print("\n ------> Se ensamblo 1 motor-chasis con 1 transmision-llantas. Se ensamblo el auto sin pintura numero",total_autos_sin_pintura)
    mutex_print.release()

    cuenta_motor_chasis = cuenta_motor_chasis - 1
    cuenta_transmision_llantas = cuenta_transmision_llantas - 1

    mutex_transmision_llantas.release()
    mutex_motor_chasis.release()

    hay_auto_sin_pintura.release()

    mutex_autos_sin_pintura.release()


def pintar_auto():
    global hay_auto_sin_pintura, hay_pintura, cuenta_pinturas, total_autos, mutex_autos, mutex_completado, numero_de_autos, mutex_print

    hay_auto_sin_pintura.acquire()
    hay_pintura.acquire()

    mutex_autos.acquire()


    total_autos = total_autos + 1  #aqui ya no se necesita una cuenta solo el total por que ya es el dato final

    mutex_print.acquire()
    print("\n >>>>>>>>>> Se pinto el auto numero",total_autos,"y esta listo para su venta.")
    mutex_print.release()

    if(total_autos > numero_de_autos - 1):
        mutex_completado.release()             #es una señalización con condicional por lo que sería un torniquete

    mutex_autos.release()
    

print("\n\n  <---- ENSAMBLAJE DE AUTOS ---->\n\n\n  Ingrese número de autos a ensamblar: ", end="")
numero_de_autos = input()

numero_de_autos = int(numero_de_autos)



for i in range(numero_de_autos*4):    #para fines ilustrativos tuve que hacer este ciclo for que lance los hilos de acuerdo al residuo del contador
    if (i%4==0):                        #de otra manera no se ve como es que se hace la paralelización
        t1 = Thread(target=constructor_motor,args=[])
        t1.start()

        t2 = Thread(target=ensamblar_motor_con_seccion_de_chasis,args=[])
        t2.start()

        t3 = Thread(target=ensamblar_transmision_con_llantas,args=[])
        t3.start()

        t_pintura = Thread(target=mezclador_pintura,args=[])
        t_pintura.start()

        te_sp = Thread(target=ensamblar_auto,args=[])
        te_sp.start()

        te_p = Thread(target=pintar_auto,args=[])
        te_p.start()

    if (i%2==0):
        t4 = Thread(target=constructor_seccion_de_chasis,args=[])
        t4.start()

    t5 = Thread(target=constructor_seccion_de_transmision,args=[])
    t5.start()

    t6 = Thread(target=constructor_llantas,args=[])
    t6.start()


mutex_completado.acquire()   #espera la señalizacion de completado en los hilos de pintar
mutex_print.acquire()
print("\n\n  ---  TODOS LOS COCHES ESTAN COMPLETADOS ---")
mutex_print.release()





































    


    
    
