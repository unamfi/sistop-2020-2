
#include <sys/sem.h>

incrementa(int *mem, int k) {
   int i;
   i=*mem; TP
   i=i+k;  TP 
   *mem=i;
}

int main() {
   key_t claveMutex;
   int   mutex;	/* semáforo */
   int  *recurso;
   char *marcaFin;

   /* obtener una clave cualquiera para el recurso ipc */
   if ((key_t) -1 == (claveMutex = ftok("ej2", 's'))) {
      fprintf(stderr, "main: Error al crear la clave con ftok()\n");
      exit(1);
   }
   /* crear del semaforo */
   if (-1 == (mutex = semCreate(claveMutex, 1))){
      fprintf(stderr, "main: No pude crear el semaforo\n");
      exit(1);
   }

   /* crear zona de memoria compartida */
   if (!crearMemoria())
      fprintf(stderr, "error de crearMemoria\n");

   recurso  = (int *) memoria ;	/* variable s.c. */
   marcaFin =  memoria + sizeof (int) ;
   *recurso =   0 ;
   *marcaFin = 'p' ;
   if (0!=fork()) {    /* proceso padre */
      int i;
      for (i=0; i< 1000; i++) {
	 semWait(mutex);
	 incrementa(recurso, -5);
	 semSignal(mutex);
      }
      while (*marcaFin != 'x') ; /* espera al hijo */

      printf("El recurso valia 0 y ahora vale %d\n", *recurso);
      if (!eliminarMemoria())   /* eliminar memoria compartida */
         fprintf(stderr, "error de eliminarMemoria\n");
      semClose(mutex);
      exit(0);
   } else {            /* proceso hijo */
      int i;

      if (-1 == (mutex = semOpen(claveMutex)))
	 fprintf(stderr, "No tengo el cualificador de mutex\n");

      for (i=0; i< 1000; i++) {
	 semWait(mutex);
	 incrementa(recurso, 5);
	 semSignal(mutex);
      }
      /* termina */
      semClose(mutex);
      *marcaFin = 'x';
      exit(0);
   }
}

}
