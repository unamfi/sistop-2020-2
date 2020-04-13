from threading import Semaphore, Thread, Lock

cuenta_motor = 0
cuenta_seccion_de_chasis = 0
cuenta_seccion_de_transmision = 0
cuenta_llantas = 0
cuenta_pinturas = 0

cuenta_motor_chasis = 0
cuenta_transmision_llantas = 0
cuenta_autos_sin_pintura = 0
cuenta_autos = 0

total_motor = 0
total_seccion_de_chasis = 0
total_seccion_de_transmision = 0
total_llantas = 0
total_pinturas = 0

total_motor_chasis = 0
total_transmision_llantas = 0
total_autos_sin_pintura = 0
total_autos = 0

mutex_print = Semaphore(1)

mutex_motor = Semaphore(1)
mutex_seccion_de_chasis = Semaphore(1)
mutex_seccion_de_transmision = Semaphore(1)
mutex_llantas = Semaphore(1)
mutex_pinturas = Semaphore(1)

mutex_motor_chasis = Semaphore(1)
mutex_transmision_llantas = Semaphore(1)
mutex_autos_sin_pintura = Semaphore(1)
mutex_autos = Semaphore(1)

hay_motor = Semaphore(0)
hay_seccion_de_chasis = Semaphore(0)
hay_seccion_de_transmision = Semaphore(0)
hay_llantas = Semaphore(0)
hay_cristales = Semaphore(0)

def constructor_motor():
    global mutex_motor, cuenta_motor, total_motor, se_puede_seccion_de_chasis

    mutex_motor.acquire()

    cuenta_motor = cuenta_motor + 1
    total_motor = total_motor + 1

    mutex_print.acquire()
    print("\n Se construyó el motor numero",total_motor)
    mutex_print.release()

    hay_motor.release()

    mutex_motor.release()


def constructor_seccion_de_chasis():
    global mutex_seccion_de_chasis, cuenta_seccion_de_chasis, total_seccion_de_chasis

    mutex_seccion_de_chasis.acquire()

    cuenta_seccion_de_chasis = cuenta_seccion_de_chasis + 1
    total_seccion_de_chasis = total_seccion_de_chasis + 1

    mutex_print.acquire()
    print("\n Se construyó la seccion de chasis numero",total_seccion_de_chasis)
    mutex_print.release()

    if(cuenta_seccion_de_chasis == 2):
        hay_seccion_de_chasis.release()

    mutex_seccion_de_chasis.release()


def ensamblar_motor_con_seccion_de_chasis():
    global hay_motor, hay_seccion_de_chasis, cuenta_motor, cuenta_seccion_de_chasis, total_motor_chasis, mutex_motor_chasis

    hay_motor.acquire()
    hay_seccion_de_chasis.acquire()

    mutex_motor.acquire()
    mutex_seccion_de_chasis.acquire()

    mutex_motor_chasis.acquire()

    total_motor_chasis = total_motor_chasis + 1

    mutex_print.acquire()
    print("\n --> Hay",cuenta_motor,"motor/es y",cuenta_seccion_de_chasis,"secciones de chasis.")
    print("\n --> Se ensamblo 1 motor con 2 secciones de chasis. Se ensamblo el motor-chasis numero",total_motor_chasis)
    mutex_print.release()

    cuenta_motor = cuenta_motor - 1
    cuenta_seccion_de_chasis = cuenta_seccion_de_chasis - 2

    mutex_motor_chasis.release()

    mutex_seccion_de_chasis.release()
    mutex_motor.release()
    




for i in range(10):
    t1 = Thread(target=constructor_motor,args=[])
    t2 = Thread(target=constructor_seccion_de_chasis,args=[])
    t3 = Thread(target=ensamblar_motor_con_seccion_de_chasis,args=[])


    t1.start()
    t2.start()
    t3.start()

































    


    
    
