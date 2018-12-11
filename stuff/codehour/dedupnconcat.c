#include <stdio.h>
#include <string.h>

int main() 
{
    int testnum, i, j, k, flag = 0;
    char strone[100], strtwo[100], dupone[100];
    scanf("%d",&testnum);
    for (i=0 ; i<testnum ; i++)
    {
        scanf("%s",&strone);
        scanf("%s",&strtwo);
        strcpy(dupone,strone);
        for (j=0 ; strone[j]!='\0' ; j++)
        {
            for (k=0 ; strtwo[k]!='\0' ; k++)
            {
                if (strone[j] == strtwo[k])
                {
                    memmove(&strone[j], &strone[j + 1], strlen(strone) - j);
                    j--;                   
                }
            }
        }
        for (j=0 ; strtwo[j]!='\0' ; j++)
        {
            for (k=0 ; dupone[k]!='\0' ; k++)
            {
                if (strtwo[j] == dupone[k])
                {
                    memmove(&strtwo[j], &strtwo[j + 1], strlen(strtwo) - j);
                    j--;
                }
            }
        }
        if (strlen(strone) + strlen(strtwo) == 0)
        {
            printf("-1\n");
        }
        else
        {
            printf("%s%s\n",strone,strtwo);
        }
    }
}