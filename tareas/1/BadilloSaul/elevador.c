#include <stdio.h> 
#include <pthread.h> 
#include <semaphore.h> 
#include <unistd.h> 
  
int piso;
sem_t mutex; 
pthread_mutex_t destino,en_sal;
pthread_cond_t piso_actual;
  
void* elevador( ) {
		printf("Se prende el elevador\n");
		pthread_mutex_lock(&en_sal);
		for(piso=0;piso<5;piso++){
			printf("Llegando al piso %d",piso);
			pthread_cond_broadcast(&piso_actual);
			pthread_mutex_unlock(&en_sal);
			sleep(10);
			pthread_mutex_lock(&en_sal);
			printf("Se mueve el elevador \n");
		}
} 
void* alumno(int* pisos) {
	printf("Llega un alumno\n");
	pthread_mutex_lock(&en_sal);
	while(piso!=pisos[0]){
		pthread_cond_wait(&piso_actual,&en_sal);
	}
	sem_wait(&mutex); 
	printf("\nEntered in floor %d..\n",pisos[0]); 
	pthread_cond_broadcast(&piso_actual);
	pthread_mutex_unlock(&en_sal);
	sleep(1);
	pthread_mutex_lock(&en_sal);
	while(piso!=pisos[1]){
		pthread_cond_wait(&piso_actual,&en_sal);
	}
	sem_post(&mutex); 
	pthread_mutex_unlock(&en_sal);
	printf("\nJust Exiting in floor %d...\n",pisos[1]); 
} 
  
  
int main() { 
    sem_init(&mutex, 0, 4); 
    pthread_t t1,t2,t3,t4,t5; 
	 int pisos[]={1,4};
    pthread_create(&t1,NULL,elevador,pisos); 
    sleep(1); 
    pthread_create(&t2,NULL,alumno,pisos); 
    sleep(1); 
    pthread_create(&t3,NULL,alumno,pisos); 
    sleep(1); 
    pthread_create(&t4,NULL,alumno,pisos); 
    sleep(1); 
    pthread_create(&t5,NULL,alumno,pisos); 
    sleep(1); 
    pthread_join(t1,NULL); 
    pthread_join(t2,NULL); 
    pthread_join(t3,NULL); 
    pthread_join(t4,NULL); 
    pthread_join(t5,NULL); 
    sem_destroy(&mutex); 
    return 0; 
} 
