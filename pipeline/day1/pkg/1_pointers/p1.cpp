#include <iostream>
#include <cstddef>

int main()
{
    void* a = 0;
    void* b = NULL;
    void* c = nullptr;
    std::cout << "a = " << a << std::endl;
    std::cout << "b = " << b << std::endl;
    std::cout << "c = " << c << std::endl;
    std::cin.get();
}
