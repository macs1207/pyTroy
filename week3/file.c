#include <stdio.h>
#include <stdlib.h>

int main()
{
    FILE *f;
    f = fopen("a.txt", "w+");

    for (int i = 10; i <= 100; i += 10)
    {
        fprintf(f, "%d\n", i);
    }
    fclose(f);
}