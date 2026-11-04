#include <iostream>

int main()
{
    int var = 8;
    int* ptr = &var;
    double* ptr2 = &var;
    std::cout << "int*    : " << ptr << std::endl;
    std::cout << "double* : " << ptr2 << std::endl;
    std::cout << "int size    = " << sizeof(int) << " bytes" << std::endl;
    std::cout << "double size = " << sizeof(double) << " bytes" << std::endl;
    std::cin.get();
}
