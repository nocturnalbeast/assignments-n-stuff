#include <stdio.h>
#include <stdlib.h>

int main()
{
    char *rootkey = "ROOT";
    char *rootval = "root";

    printf("The current user is %s.\n",getenv("USER"));
    printf("The home directory of the current user is %s.\n",getenv("HOME"));
    printf("The present working directory of this terminal is %s.\n",getenv("PWD"));
    printf("The paths set in the $PATH variable is %s.\n",getenv("PATH"));

    setenv(rootkey,rootval,1);

    printf("The newly set variable is ROOT and its values is %s.\n",getenv("ROOT"));
}