#include <iostream>

struct Vec3
{
    float x, y, z;
};

float cross2D(float v1, float v2, float w1, float w2)
{
    return v1 * w2 - v2 * w1;
}

Vec3 cross(Vec3 v, Vec3 w)
{
    return { v.y * w.z - v.z * w.y,
             v.z * w.x - v.x * w.z,
             v.x * w.y - v.y * w.x };
}

float dot(Vec3 a, Vec3 b)
{
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

int main()
{
    std::cout << "2D  v x w = " << cross2D(-3, 1, 2, 1) << std::endl;
    std::cout << "2D  w x v = " << cross2D(2, 1, -3, 1) << std::endl;
    std::cout << "2D  3v x w = " << cross2D(-9, 3, 2, 1) << std::endl;

    Vec3 v = { 0, 0, 2 };
    Vec3 w = { 0, 2, 0 };
    Vec3 c = cross(v, w);
    std::cout << "3D  v x w = (" << c.x << ", " << c.y << ", " << c.z << ")" << std::endl;
    std::cout << "c . v = " << dot(c, v) << "   c . w = " << dot(c, w) << std::endl;
    std::cin.get();
}
