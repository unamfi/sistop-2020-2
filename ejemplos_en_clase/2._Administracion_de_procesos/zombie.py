#!/usr/bin/python3

import os
import time

pid = os.fork()
if pid > 0:
    # Soy el proceso padre
    print("Soy el proceso padre. Mi PID es %d y el del hijo es %d" %
          (os.getpid(), pid))
    time.sleep(20)

else:
    # Soy el proceso hijo
    print("Soy el proceso hijo. Mi PID es %d y el resultado del fork es %d" %
          (os.getpid(), pid))
    time.sleep(10)

exit(0)
