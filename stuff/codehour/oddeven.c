#include <stdio.h>

int main() 
{
    int testnum, num, i;
    scanf("%d",&testnum);
    for(i=0;i<testnum;i++)
    {
        scanf("%d",&num);
        printf(num%2==0?"even\n":"odd\n");
    }
}
