#include <stdio.h>
#include <stdlib.h>

int main() {

    int i, countarr[10];
    char inputbuf[1000];
    fgets (inputbuf, 1000, stdin);
    for (i=0;i<10;i++)
        countarr[i]=0;
    for (i=0;inputbuf[i]!='\0';i++)
    {
        if ((inputbuf[i] >= '0') && (inputbuf[i] <= '9'))
            countarr[inputbuf[i]-48]++;
    }
    for (i=0;i<10;i++)
        printf("%d ",countarr[i]);
    return 0;
    
}

