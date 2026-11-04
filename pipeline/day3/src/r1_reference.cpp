#include <iostream>

int main()
{
    int a = 5;
    int& ref = a;

    ref = 2;
    std::cout << "a    = " << a << std::endl;
    std::cout << "&a   = " << &a << std::endl;
    std::cout << "&ref = " << &ref << std::endl;
    std::cin.get();
}
