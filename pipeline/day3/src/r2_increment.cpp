#include <iostream>

void IncrementCopy(int value)
{
    value++;
}

void IncrementPointer(int* value)
{
    (*value)++;
}

void IncrementReference(int& value)
{
    value++;
}

int main()
{
    int a = 5;

    IncrementCopy(a);
    std::cout << "copy:      a = " << a << std::endl;

    IncrementPointer(&a);
    std::cout << "pointer:   a = " << a << std::endl;

    IncrementReference(a);
    std::cout << "reference: a = " << a << std::endl;
    std::cin.get();
}
