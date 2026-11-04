#include <iostream>

struct Vec3
{
    float x, y, z;
};

Vec3 cross(Vec3 a, Vec3 b)
{
    return { a.y * b.z - a.z * b.y,
             a.z * b.x - a.x * b.z,
             a.x * b.y - a.y * b.x };
}

float dot(Vec3 a, Vec3 b)
{
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

void check(Vec3 a, Vec3 b)
{
    Vec3 c = cross(a, b);
    std::cout << "[" << a.x << ", " << a.y << ", " << a.z << "] x ["
              << b.x << ", " << b.y << ", " << b.z << "] = ["
              << c.x << ", " << c.y << ", " << c.z << "]"
              << "    c.a = " << dot(c, a) << "  c.b = " << dot(c, b) << std::endl;
}

int main()
{
    check({ 1, -7, 1 }, { 5, 2, 4 });
    check({ 1, 0, 0 }, { 0, 1, 0 });
    check({ 0, 1, 0 }, { 1, 0, 0 });
    check({ 2, 3, 4 }, { 5, 6, 7 });
    check({ 3, -3, 1 }, { 4, 9, 2 });
    std::cin.get();
}
