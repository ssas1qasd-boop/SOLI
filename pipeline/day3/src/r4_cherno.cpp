#include <iostream>

#define LOG(x) std::cout << x << std::endl

void Increment(int& value)
{
    value++;
}

int main()
{
    int a = 5;
    int b = 8;

    int& ref = a;
    ref = 2;
    LOG(a);

    Increment(a);
    LOG(a);

    int* ptr = &a;
    *ptr = 2;
    LOG(a);

    ptr = &b;
    *ptr = 1;
    LOG(b);

    std::cin.get();
}
