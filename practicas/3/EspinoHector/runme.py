from hola import hablar
import threading
def trabajar():
    hablar("Estamos generando un pyc.")
    print(threading.current_thread().name)
for i in range(10):
    x=threading.Thread(target=trabajar).start()
