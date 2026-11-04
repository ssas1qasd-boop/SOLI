#include <stdio.h>
#include <string.h>
int compute(const char* lhs, const char* rhs)
{
size_t lhs_length = strlen(lhs);
size_t rhs_length = strlen(rhs);
if (lhs_length != rhs_length)
return -1;
int distance = 0;
for (size_t i = 0; i < lhs_length; i++)
{
if (lhs[i] != rhs[i])
distance++;
}
return distance;
}
int main(void)
{
printf("%d\n", compute("GAGCCTACTAACGGGAT", "CATCGTAATGACGGCCT"));
printf("%d\n", compute("GGACTGA", "GGACTGA"));
printf("%d\n", compute("AATG", "AAA"));
return 0;
}