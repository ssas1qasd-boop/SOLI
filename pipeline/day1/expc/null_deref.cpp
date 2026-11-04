#include <iostream>

int main()
{
    int var = 8;
    int* ptr = nullptr;
    std::cout << "before: var = " << var << std::endl;
    *ptr = 10;
    std::cout << "after:  var = " << var << std::endl;
    std::cin.get();
}
