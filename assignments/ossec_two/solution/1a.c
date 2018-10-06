#include <stdio.h>
#include <stdlib.h>

int main()
{
    printf("The current user is %s.\n",getenv("USER"));
    printf("The home directory of the current user is %s.\n",getenv("HOME"));
    printf("The present working directory of this terminal is %s.\n",getenv("PWD"));
    printf("The paths set in the $PATH variable is %s.\n",getenv("PATH"));
}