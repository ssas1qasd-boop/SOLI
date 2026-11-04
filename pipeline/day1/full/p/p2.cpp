#include <iostream>

int main()
{
    int var = 8;
    void* ptr = &var;
    std::cout << "var  = " << var << std::endl;
    std::cout << "&var = " << &var << std::endl;
    std::cout << "ptr  = " << ptr << std::endl;
    std::cin.get();
}
