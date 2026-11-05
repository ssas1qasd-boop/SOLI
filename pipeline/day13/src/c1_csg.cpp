#include <iostream>
#include <iomanip>

struct Vec3
{
    float x, y, z;
};

bool InSphere(Vec3 p)
{
    return p.x * p.x + p.y * p.y + p.z * p.z <= 1.0f;
}

bool InBox(Vec3 p)
{
    return p.x >= 0.0f && p.x <= 2.0f && p.y >= -0.5f && p.y <= 0.5f && p.z >= -0.5f && p.z <= 0.5f;
}

bool Union(Vec3 p)
{
    return InSphere(p) || InBox(p);
}

bool Intersect(Vec3 p)
{
    return InSphere(p) && InBox(p);
}

bool Difference(Vec3 p)
{
    return InSphere(p) && !InBox(p);
}

void Row(const char* name, bool (*inside)(Vec3))
{
    std::cout << name;
    for (float x = -1.5f; x <= 2.51f; x += 0.5f)
        std::cout << std::setw(5) << (inside({ x, 0.0f, 0.0f }) ? "#" : ".");
    std::cout << std::endl;
}

int main()
{
    std::cout << "x:         ";
    for (float x = -1.5f; x <= 2.51f; x += 0.5f)
        std::cout << std::setw(5) << x;
    std::cout << std::endl;
    Row("sphere A:  ", InSphere);
    Row("box B:     ", InBox);
    Row("A union B: ", Union);
    Row("A inter B: ", Intersect);
    Row("A minus B: ", Difference);
    Vec3 q = { 0.5f, 0.8f, 0.0f };
    std::cout << "(0.5, 0.8, 0): A " << InSphere(q) << ", B " << InBox(q) << ", A minus B " << Difference(q) << std::endl;
    return 0;
}
