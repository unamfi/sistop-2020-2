from threading import Thread
import time
from random import randint, random, uniform

#start = time.perf_counter()

def diabetes(estudio, list):
    print("Calculando procesos para la diabétes")
    time.sleep(5)
    print("Verificar niveles para: ")
    if estudio == 1:
        nivel1 = uniform(5.24,9.57)
        print(f"Hemoglobina glicosilada. Nivel:  {nivel1:.4f} HbA1c")
        list.append(f"Hemoglobina glicosilada. Nivel:  {nivel1:.4f} HbA1c")
        if nivel1 <= 6:
            print("H-Dx : Nivel normal.")
            list.append("H-Dx : Nivel normal.")
        elif nivel1 > 6 and nivel1 <= 7:
            print("H-Dx : Nivel objetivo.")
            list.append("H-Dx : Nivel objetivo.")
        elif nivel1 >= 8:
            print("H-Dx : Requiere intervención.")
            list.append("H-Dx : Requiere intervención.")
    elif estudio == 2:
        nivel2 = uniform(80.55,158.30)
        print(f"Glucemia prepandial. Nivel:  {nivel2:.4f} (mg/dl)")
        list.append(f"Glucemia prepandial. Nivel:  {nivel2:.4f} (mg/dl)")
        if nivel2 <= 110:
            print("G-Dx : Nivel normal.")
            list.append("G-Dx : Nivel normal.")
        elif nivel2 >= 110 and nivel2 <= 130:
            print("G-Dx : Nivel objetivo.")
            list.append("G-Dx : Nivel objetivo.")
        elif nivel2 >= 150 or nivel2 <= 90:
            print("G-Dx : Requiere intervención.")
            list.append("G-Dx : Requiere intervención.")


def perfiles_comunes():
    time.sleep(1)
    print('Hey')

def main():
    list = []
    start = time.perf_counter()
    t = Thread(target=diabetes, args=(randint(1,2),list,))
    s = Thread(target=diabetes, args=(randint(1,2),list,))

    t.start()
    s.start()

    t.join()
    s.join()

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} second(s)')
    return list
main()