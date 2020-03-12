#include <stdio.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <pthread.h>
#include <stdlib.h>

#define BUFSIZE 10

#define MUTEX 0
#define FULL 1
#define EMPTY 2

int semid;




int sem_create(int nsems) { 
	int  id;
	key_t key = 1234;
	int semflg = IPC_CREAT | 0666;
	id = semget(key, nsems, semflg);
	if(id < 0)
	{
		perror("semget:");
		exit (1);
	}
	return id;
}

void sem_initialise(int semno, int val) {
	union semun un;
	un.val = val;
	if(semctl(semid, semno, SETVAL, un) < 0)
	{
	//	printf("%d\n", semno);
		perror("semctl:");
		exit(2);
	}
}

void *producer(void *id);
void *consumer(void *id);

void wait(int semno);
void signal(int semno);

int buffer[BUFSIZE], data;
int in = 0;
int out = 0;

int i = 10000;
int j = 10000;

int	main	(int	argc,	char	*argv[])	{
	semid = sem_create(3);
	sem_initialise(MUTEX, 1);
	sem_initialise(FULL, 0);
	sem_initialise(EMPTY, 10);

	pthread_t prod, cons;	
	
	pthread_create(&prod, NULL, producer, (void *)semid);
	pthread_create(&cons, NULL, consumer, (void *)semid);
	
	pthread_exit(NULL);
	return	0;
}

void *producer(void *id) {
	int semid = (int)(unsigned long) id;
	data = 0;
	while(i--) {
		wait(EMPTY);
		wait(MUTEX);

		/** Critical Section **/
		buffer[in] = data;
		in = (in + 1) % BUFSIZE;
		data = (data + 1) % BUFSIZE;
		printf("P:%d\n", data);
		//printf("P\n");
		signal(MUTEX);
		signal(FULL);
	}
	pthread_exit(NULL);
}

void *consumer(void *id) {
	int semid = (int)(unsigned long) id;
	while(j--)
	{
	wait(FULL);
	wait(MUTEX);
	
	/** Critical Section 	**/	
	data = buffer[out];
	out = (out + 1) % BUFSIZE;
	printf("C:%d\n", data);
	/** 			**/
	
	signal(MUTEX);
	signal(EMPTY);
	}	
	
	pthread_exit(NULL);
}

void wait(int semno) {
	struct sembuf buf;
	buf.sem_num = semno;
	buf.sem_op = -1;
	buf.sem_flg = 0;
	if(semop(semid, &buf, 1) < 0) {
		perror("semop:");
		exit(2);
	}
}

void signal(int semno) {
	struct sembuf buf;
	buf.sem_num = semno;
	buf.sem_op = 1;
	buf.sem_flg = 0;
	if(semop(semid, &buf, 1) < 0)
	{
		perror("semop:");
		exit(2);
	}
}
