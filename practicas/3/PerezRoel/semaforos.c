#include <stdio.h>
#include <pthread.h> //biblioteca de hilos
#include <semaphore.h> //biblioteca de semaforos
#include <unistd.h>
/*
  DEBE compilarse con -lpthread y -lrt 
*/

sem_t mutex; // declaracion de semaforo que actuara como mutex

void* thread(void* arg)
{
	//lo adquiere
	sem_wait(&mutex);
	printf("\n Entro...\n");

	//seccion critica 
	sleep(4); //duerme cuatro segundos

	//lo libera
	printf("\n Saliendo...\n");
	sem_post(&mutex);
}

int main()
{
	/*
	Se inicializa el mutex como un semaforo. Sus parametros son:
	un apuntador a la variable sem_t, mutex
	la variable 0 indica que que el semaforo es compartido entre los hilos de un proceso
	la variable 1 indica que es el entero con el que se inicializa
	*/
	sem_init(&mutex,0,1); 

	pthread_t t1,t2; //se declaran los hilos
	pthread_create(&t1,NULL,thread,NULL); //se crea un hilo
	sleep(2); // duerme 2 segundos
	pthread_create(&t2,NULL,thread,NULL); //se crea otro hilo, 2 segundos despues
	pthread_join(t1,NULL);
	pthread_join(t2,NULL);
	sem_destroy(&mutex);
	return 0;

}
