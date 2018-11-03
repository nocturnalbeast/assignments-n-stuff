#include <stdio.h>

int main() 
{
    int testnum, i, num, j;
    int arr[100];
    scanf("%d",&testnum);
    for(i=0;i<testnum;i++)
    {
        scanf("%d",&num);
        for(j=0;j<num;j++)
        {
            scanf("%d",&arr[j]);
        }
        for(j=num-1;j>=0;j--)
        {
            printf("%d ",arr[j]);
        }
        printf("\n");
    }
}
