#include <stdio.h>

int main(void)
{
    int arr[4] = { 10, 20, 30, 40 };
    int* p = arr;

    for (int i = 0; i < 4; i++)
    {
        printf("p = %p   *p = %d\n", (void*)p, *p);
        p++;
    }
    return 0;
}
