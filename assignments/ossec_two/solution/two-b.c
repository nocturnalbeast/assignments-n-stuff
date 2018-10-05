#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

void *printvar(void *args) {
	int *getvar;
	getvar = (int *)args;
	printf("The value you passed is %d.\n", *getvar);
	pthread_exit(NULL);
}

int main() {

	int *passptr;
	pthread_t tid;
	char cont;
	
	cont = 'y';
	while(cont == 'y')
	{
		printf("Enter the number you want to pass to the thread:");
		passptr = (int *)malloc(sizeof(passptr));
		scanf("%d", passptr);
		pthread_create(&tid, NULL, printvar, (void *)passptr);
		pthread_join(tid, NULL);
		printf("\nDo you want to continue (y/n)?");
		scanf("%c", cont);
	}
	
	return 0;
}