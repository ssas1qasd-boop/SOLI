#include <iostream>
#include <cmath>

struct Point
{
    float x, y;
};

const float Pi = 3.14159265f;

float ToRadians(float degrees)
{
    return degrees * Pi / 180.0f;
}

Point RotateZ(Point p, float radians)
{
    float c = std::cos(radians), s = std::sin(radians);
    return { p.x * c - p.y * s, p.x * s + p.y * c };
}

float Round2(float v)
{
    return std::round(v * 100) / 100 + 0.0f;
}

void PrintTurn(const Point* points, int count, float degrees)
{
    std::cout << "turn " << degrees << ":";
    for (int i = 0; i < count; i++)
    {
        Point q = RotateZ(points[i], ToRadians(degrees));
        std::cout << " (" << Round2(q.x) << ", " << Round2(q.y) << ")";
    }
    std::cout << std::endl;
}

int main()
{
    const Point triangle[3] = { { 1, 0 }, { 0, 1 }, { -1, 0 } };
    for (float degrees : { 30.0f, 60.0f, 90.0f })
        PrintTurn(triangle, 3, degrees);
    return 0;
}
