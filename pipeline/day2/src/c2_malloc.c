#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int count = 5;
    int* numbers = malloc(count * sizeof(int));
    if (numbers == NULL)
        return 1;

    for (int i = 0; i < count; i++)
        numbers[i] = i * 10;

    for (int i = 0; i < count; i++)
        printf("numbers[%d] = %d\n", i, numbers[i]);

    free(numbers);
    return 0;
}
