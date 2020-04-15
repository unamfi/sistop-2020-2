from threading import Thread
import time

start = time.perf_counter()

def hacer():
    time.sleep(3)
    print('Hola')
def hacer_otracosa():
    time.sleep(1)
    print('Hey')

t = Thread(target=hacer)
t.start()
s = Thread(target=hacer_otracosa)
s.start()

t.join()
s.join()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')