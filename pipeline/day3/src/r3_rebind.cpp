#include <iostream>

int main()
{
    int a = 5;
    int b = 8;

    int& ref = a;
    ref = b;
    std::cout << "after ref = b:  a = " << a << "  b = " << b << std::endl;

    int* ptr = &a;
    *ptr = 2;
    ptr = &b;
    *ptr = 1;
    std::cout << "after pointer:  a = " << a << "  b = " << b << std::endl;
    std::cin.get();
}
