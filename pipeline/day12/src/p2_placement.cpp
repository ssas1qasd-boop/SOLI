#include <iostream>
#include <new>

struct Vector3
{
    float x, y, z;

    Vector3(float x, float y, float z)
        : x(x), y(y), z(z)
    {
        std::cout << "Vector3(" << x << ", " << y << ", " << z << ") at " << this << std::endl;
    }

    ~Vector3()
    {
        std::cout << "~Vector3() at " << this << std::endl;
    }
};

int main()
{
    int* b = new int[50];
    std::cout << "new int[50] at " << b << std::endl;

    Vector3* v = new (b) Vector3(1.0f, 2.0f, 3.0f);
    std::cout << "placement new: v = " << v << ", same address as b: " << (v == (void*)b ? "yes" : "no") << std::endl;
    std::cout << "b[0] as float = " << *(float*)b << std::endl;

    v->~Vector3();
    delete[] b;

    Vector3* h = new Vector3(4.0f, 5.0f, 6.0f);
    delete h;
    return 0;
}
