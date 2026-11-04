#include <iostream>

void SwapValue(int a, int b)
{
    std::cout << "  SwapValue got copies at:    " << &a << " and " << &b << std::endl;
    int temp = a;
    a = b;
    b = temp;
}

void SwapPointer(int* a, int* b)
{
    std::cout << "  SwapPointer got addresses:  " << a << " and " << b << std::endl;
    int temp = *a;
    *a = *b;
    *b = temp;
}

void SwapReference(int& a, int& b)
{
    std::cout << "  SwapReference got the same: " << &a << " and " << &b << std::endl;
    int temp = a;
    a = b;
    b = temp;
}

int main()
{
    int x = 10, y = 20;
    std::cout << "x lives at " << &x << ", y lives at " << &y << std::endl;

    SwapValue(x, y);
    std::cout << "after SwapValue:     x = " << x << ", y = " << y << std::endl;

    SwapPointer(&x, &y);
    std::cout << "after SwapPointer:   x = " << x << ", y = " << y << std::endl;

    SwapReference(x, y);
    std::cout << "after SwapReference: x = " << x << ", y = " << y << std::endl;
}
