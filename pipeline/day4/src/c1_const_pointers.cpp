#include <iostream>

int main()
{
    const int MAX_AGE = 90;
    std::cout << "MAX_AGE = " << MAX_AGE << std::endl;

    int* a = new int(5);
    *a = 2;
    std::cout << "int*:              *a = " << *a << std::endl;

    const int* b = a;
    b = &MAX_AGE;
    std::cout << "const int*:        *b = " << *b << std::endl;

    int* const c = new int(5);
    *c = 2;
    std::cout << "int* const:        *c = " << *c << std::endl;

    const int* const d = &MAX_AGE;
    std::cout << "const int* const:  *d = " << *d << std::endl;

    delete a;
    delete c;
    std::cin.get();
}
