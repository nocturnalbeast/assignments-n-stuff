#include <pthread.h>
#include <stdio.h>

void main()
{
    pthread_t threadid;
    int p_err;

    printf("Creating a thread...\n");
    p_err = pthread_create(&threadid,NULL,threadfunc,NULL);
    pthread_join(&threadid,NULL);
    printf("Thread is dead!\n");

    return(0);
}

int threadfunc()
{
    printf("Hello world!\n");
    return(0);
}