/*
Murrieta Villegas Alfonso

Programa basado en código de Jorge Duran de Somos Binarios

NOTA:
Manera de usar semget http://pubs.opengroup.org/onlinepubs/7908799/xsh/semget.html

*/

#include <stdio.h>
#include <stdlib.h>

//Bibliotecas para el manejo de semaforos
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ipc.h>
#include <sys/sem.h>

/*
Funciones propias de los semáforos 
-inicializar -> initSem
-decrementar -> wait
-incrementar -> doSignal 

*/


void doSignal(int semid, int numSem) {
    struct sembuf sops; //Signal
    sops.sem_num = numSem;
    sops.sem_op = 1;
    sops.sem_flg = 0;

    if (semop(semid, &sops, 1) == -1) {
        perror(NULL);
        error("Error al hacer Signal");
    }
}

void doWait(int semid, int numSem) {
    struct sembuf sops;
    sops.sem_num = numSem; /* Sobre el primero, ... */
    sops.sem_op = -1; /* ... un wait (resto 1) */
    sops.sem_flg = 0;

    if (semop(semid, &sops, 1) == -1) {
        perror(NULL);
        error("Error al hacer el Wait");
    }
}

void initSem(int semid, int numSem, int valor) { 

    if (semctl(semid, numSem, SETVAL, valor) < 0) {        
    perror(NULL);
        error("Error iniciando semaforo");
    }
}

void error(char* errorInfo) {
    fprintf(stderr,"%s",errorInfo);
    exit(1);
}



//###############################

int main() {
    puts("Sincronizacion con Semaforos ");
    int semaforo;
    

    //Creamos un semaforo y damos permisos para compartirlo
    if((semaforo=semget(IPC_PRIVATE,1,IPC_CREAT | 0700))<0) {
        perror(NULL);
        error("Semaforo: semget");
        }

    initSem(semaforo,0,1);
    puts("Hay una plaza libre");  

    switch (fork())
    {
        case -1:
            error("Error en el fork"); 

        case 0:  /* Hijo */
            doWait(semaforo,0);
            puts("Entro el hijo, el padre espera");
            sleep(5);
            puts("El hijo sale");
            doSignal(semaforo,0);
            exit(0);

        default: /* Padre */
            doWait(semaforo,0);
            puts("Entro el padre, el hijo espera");
            sleep(5);
            puts("El padre sale");
            doSignal(semaforo,0);
    }       
    
    sleep(20);
    
    //Liberación del semaforo
    if ((semctl(semaforo, 0, IPC_RMID)) == -1) {
        perror(NULL);
        error("Semaforo borrando");
    }

return 0;
}








