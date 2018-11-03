#include <stdio.h>

int main() 
{
    int testcases, num, i, j;
    scanf("%d",&testcases);
    num = testcases;
    for(i=0;i<testcases;i++)
    {
        scanf("%d",&num);
        for(j=1;j<=10;j++)
            printf("%d ",num*j);
        printf("\n");
    }
}
