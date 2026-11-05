#include <iostream>

struct Vector2
{
    float x, y;
};

int main()
{
    int a = 2;
    int b = a;
    b = 3;
    std::cout << "int:      a = " << a << ", b = " << b << std::endl;

    Vector2 va = { 2, 3 };
    Vector2 vb = va;
    vb.x = 5;
    std::cout << "struct:   va.x = " << va.x << ", vb.x = " << vb.x << ", &va = " << &va << ", &vb = " << &vb << std::endl;

    Vector2* pa = new Vector2();
    Vector2* pb = pa;
    pb->x = 5;
    std::cout << "pointer:  pa->x = " << pa->x << ", pb->x = " << pb->x << ", pa == pb: " << (pa == pb ? "yes" : "no") << std::endl;
    delete pa;

    Vector2& ra = va;
    ra.y = 9;
    std::cout << "reference: va.y = " << va.y << " (ra is va, nothing was copied)" << std::endl;
    std::cout << "sizeof(Vector2) = " << sizeof(Vector2) << ", sizeof(Vector2*) = " << sizeof(Vector2*) << std::endl;
    return 0;
}
