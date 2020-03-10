/*
Valdespino Mendieta Joaquin
programa de : Fernandez Gaspar
si desea saber mas acerca del problema de concurrencia
recuperado de:https://poesiabinaria.net/2014/02/concurrencia-cuando-varios-hilos-threads-pelean-por-el-acceso-a-un-recurso-ejemplos-en-c/

para compilarlo se requiere gcc archivo -pthread
*/

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

struct thread_vars_t
{
  int number;
  pthread_mutex_t mutex;
};

int numberExists(int arr[], int current)
{
  int i;

  for (i=0; i<current; ++i)
    {
      if (arr[current]==arr[i])
    return 1;
    }

  return 0;
}

void numberSearch()
{
  /* A time taking task */
  int numbers[100];
  int i;

  for (i=0; i<100; ++i)
    {
      numbers[i] = rand()%101;
      while (numberExists(numbers, i))
    numbers[i] = rand()%101;
    }
}


void *newtask(void *_number)
{
  struct thread_vars_t *vars = _number;

  /* BLOCK */
  pthread_mutex_lock(&vars->mutex);
  /* BLOCK */

  int number = vars->number;
  numberSearch();
  vars->number = number+1;

  /* UNBLOCK */
  pthread_mutex_unlock(&vars->mutex);
  /* UNBLOCK */

  printf ("THREAD: number = %d\n", vars->number);

  pthread_exit(NULL);
}

int main (int argc, char *argv[])
{
   pthread_t thread;
   int rc;
   int i;
   struct thread_vars_t *vars = malloc (sizeof(struct thread_vars_t));

   pthread_mutex_init(&vars->mutex, NULL);
   vars->number = 0;

   printf ("Main process just started.\n");
   for (i=0; i<10; ++i)
     {
       rc = pthread_create(&thread, NULL, newtask, vars);
       if (rc)
     {
       printf("ERROR in pthread_create(): %d\n", rc);
       exit(-1);
     }
     }

   printf ("Main process about to finish.\n");
   /* Last thing that main() should do */
   pthread_exit(NULL);
}
