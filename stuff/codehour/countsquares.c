#include <stdio.h>
#include <math.h>

int main() 
{
    int testnum, i, num;
    float root;
    scanf("%d",&testnum);
    for(i=0;i<testnum;i++)
    {
        scanf("%d",&num);
        root = sqrt(num);
        printf("%d\n",(int)ceil(root)-1);
    }
}
