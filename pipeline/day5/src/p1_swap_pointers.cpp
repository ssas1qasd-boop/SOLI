// swap two numbers in C++ using pointers

#include <iostream>
using namespace std;

int main()
{
    int x = 10, y = 20;

    void swap(int* p, int* q);

    cout << "Before swapping" << endl;
    cout << "x = " << x << " and y = " << y << endl;

    swap(&x, &y);

    cout << "Value after swapping" << endl;
    cout << "x = " << x << " and y = " << y << endl;
}

void swap(int* a, int* b)
{
    int temp;
    temp = *a;
    *a = *b;
    *b = temp;
}
