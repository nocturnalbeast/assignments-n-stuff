#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

pthread_mutex_t mutexvar;

void *printvar(void *args) {
	pthread_mutex_lock(&mutexvar);
	int *getvar;
	getvar = (int *)args;
	printf("The value you passed is %d.\n", *getvar);
	pthread_mutex_unlock(&mutexvar);
	pthread_exit(NULL);
}

int main() {

	int *passptr;
	pthread_t tid;
	int cont;
	
	cont = 1;
	while(cont == 1)
	{
		printf("Enter the number you want to pass to the thread:");
    	pthread_mutex_lock(&mutexvar);
		passptr = (int *)malloc(sizeof(passptr));
		scanf("%d", passptr);
    	pthread_mutex_unlock(&mutexvar);
		pthread_create(&tid, NULL, printvar, (void *)passptr);
		pthread_join(tid, NULL);
		printf("\nDo you want to continue?\nEnter 1 to continue, or any other number to exit.");
		scanf("%d",&cont);
	}
	
	return 0;
}