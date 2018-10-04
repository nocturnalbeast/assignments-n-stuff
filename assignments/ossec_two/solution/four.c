#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

pthread_mutex_t mutexvar;

struct mul_values{
    int one, two;
};

void *multiply(void *args) {
    struct mul_values *getvar;
    int one, two;
    pthread_mutex_lock(&mutexvar);
    int *result = malloc(sizeof(int));
    getvar = (struct mul_values *)args;
    one = getvar->one;
    two = getvar->two;
    pthread_mutex_unlock(&mutexvar);
    *result = one*two;
    pthread_exit(result);
}

int main() {

    int one, two;
    pthread_t tid;
    struct mul_values *passptr;
    void *result;

    pthread_mutex_init(&mutexvar, NULL);

    printf("Enter the two operands:\n");
    scanf("%d", &one);
    scanf("%d", &two);

    pthread_mutex_lock(&mutexvar);
    passptr = (struct mul_values *)malloc(sizeof(passptr));
    passptr->one = one;
    passptr->two = two;
    pthread_mutex_unlock(&mutexvar);

    pthread_create(&tid, NULL, multiply, (void *)passptr);
    pthread_join(tid, &result);

    printf("The product of the two numbers is %d.", *(int*)result);
   
    return 0;
}