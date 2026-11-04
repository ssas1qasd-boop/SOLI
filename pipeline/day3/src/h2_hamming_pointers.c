#include <stdio.h>

int compute(const char* lhs, const char* rhs)
{
    if (!lhs || !rhs)
        return -1;

    int distance = 0;
    for (; *lhs && *rhs; lhs++, rhs++)
    {
        if (*lhs != *rhs)
            distance++;
    }

    return (*lhs || *rhs) ? -1 : distance;
}

int main(void)
{
    printf("%d\n", compute("GAGCCTACTAACGGGAT", "CATCGTAATGACGGCCT"));
    printf("%d\n", compute("GGACTGA", "GGACTGA"));
    printf("%d\n", compute("AATG", "AAA"));
    printf("%d\n", compute(NULL, "AAA"));
    return 0;
}
