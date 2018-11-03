#include <stdio.h>

int main() 
{
    int testnum, i, num, lcl_sum;
    scanf("%d",&testnum);
    for(i=0;i<testnum;i++)
    {
        scanf("%d",&num);
        lcl_sum = 0;
        while(num > 0)
        {
            lcl_sum = lcl_sum + (num%10);
            num = num/10;
        }
        printf("%d\n",lcl_sum);
    }
}
