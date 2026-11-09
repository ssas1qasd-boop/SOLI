#include <iostream>
#include <cmath>

struct Vec4
{
    float x, y, z, w;
};

float Dot(Vec4 a, Vec4 b)
{
    return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w;
}

struct Mat4
{
    Vec4 row[4];
};

Vec4 Apply(const Mat4& m, Vec4 v)
{
    return { Dot(m.row[0], v), Dot(m.row[1], v), Dot(m.row[2], v), Dot(m.row[3], v) };
}

Mat4 Translation(float x, float y, float z)
{
    return { { { 1, 0, 0, x }, { 0, 1, 0, y }, { 0, 0, 1, z }, { 0, 0, 0, 1 } } };
}

int main()
{
    Vec4 a = { 1, 2, 3, 0 };
    Vec4 b = { 4, 5, 6, 0 };
    std::cout << "dot((1, 2, 3), (4, 5, 6)) = " << Dot(a, b) << std::endl;

    Mat4 T = Translation(0.5f, -0.25f, 0.0f);
    Vec4 v = { -1, -1, 0, 1 };
    std::cout << "row 0 . v = " << Dot(T.row[0], v) << ", row 1 . v = " << Dot(T.row[1], v) << ", row 2 . v = " << Dot(T.row[2], v) << ", row 3 . v = " << Dot(T.row[3], v) << std::endl;

    Vec4 triangle[3] = { { -1, -1, 0, 1 }, { 1, -1, 0, 1 }, { 0, 1, 0, 1 } };
    for (int frame = 0; frame < 4; frame++)
    {
        float scale = std::sin(frame * 3.14159265f / 2.0f);
        Mat4 M = Translation(scale * 0.5f, 0.0f, 0.0f);
        std::cout << "frame " << frame << ", offset " << std::round(scale * 0.5f * 100) / 100 + 0.0f << ":";
        for (Vec4 p : triangle)
        {
            Vec4 q = Apply(M, p);
            std::cout << " (" << std::round(q.x * 100) / 100 + 0.0f << ", " << q.y << ")";
        }
        std::cout << std::endl;
    }
    return 0;
}
