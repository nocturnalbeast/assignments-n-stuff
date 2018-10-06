#include <stdio.h>
#include <semaphore.h>
#include <pthread.h>

int buf;
sem_t m,t;

void *product (void *args) {
    
    int temp;
    
    sem_wait(&t);
    temp = buf;
    sem_post(&m);
    
    sem_wait(&t);
    buf *= temp;
    sem_post(&m);

}

int main() {

    pthread_t tid;
    int i;

    sem_init(&t, 0, 0);
    sem_init(&m, 0, 1);

    pthread_create(&tid, NULL, product, NULL);
    for (i=0 ; i<2 ; i++) {
        sem_wait(&m);
        printf("Enter the operand:");
        scanf("%d", &buf);
        sem_post(&t);
    }

    sem_wait(&m);
    printf("\nThe product is %d.",buf);

}