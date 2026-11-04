#include <iostream>

int start()
{
    int var = 8;
    int* ptr = &var;
    std::cout << "before: var = " << var << std::endl;
    *ptr = 10;
    std::cout << "after:  var = " << var << std::endl;
    std::cin.get();
}
