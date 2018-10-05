#include <stdio.h>
#include <pthread.h>

void *greet() {
	printf("Hello, world!\n");
}

int main() {

	pthread_t tid;

	printf("A new thread will now greet you.\n");
	
	pthread_create(&tid, NULL, greet, NULL);
	pthread_join(tid, NULL);
	
	return 0;

}