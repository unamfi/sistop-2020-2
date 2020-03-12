/*
en este programa se muestra un ejemplo sencillo de la utilizacion 
de semaforos en forma de mutex
donde un hilo sumara 1000 veces 1 a un contador
mientras que otro hilo restara 1000 veces 1 al contador
al final del programa deberia de mostrar el contador en 0

*/
#include <stdio.h>
#include <semaphore.h>
#include <pthread.h>

#define LOOP 1000
static void * thread_1_function(void* arg);
static void * thread_2_function(void* arg);

static int contador = 0;

sem_t sem1;

int main (void)
{
    pthread_t thread_1, thread_2;

    sem_init(&sem1, 0, 1);

    pthread_create(&thread_1, NULL, *thread_1_function, NULL);
    pthread_create(&thread_2, NULL, *thread_2_function, NULL);

    pthread_join(thread_1, NULL);
    pthread_join(thread_2, NULL);

    printf("valor contador %d \n", contador);
    return 0;
}

static void * thread_1_function(void* arg)
{
    for(int i = 0; i< LOOP; i++)
    {
        sem_wait(&sem1);
        contador += 1;
        sem_post(&sem1);
    }
}

static void * thread_2_function(void* arg)
{
   for(int i = 0; i< LOOP; i++)
    {
        sem_wait(&sem1);
        contador -= 1;
        sem_post(&sem1);
    } 
}