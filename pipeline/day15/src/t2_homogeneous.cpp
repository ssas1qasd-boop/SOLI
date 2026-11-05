#include <iostream>
#include <cmath>

struct Mat3
{
    float m[3][3];
};

struct Vec3
{
    float x, y, w;
};

Mat3 Multiply(const Mat3& a, const Mat3& b)
{
    Mat3 r = {};
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            for (int k = 0; k < 3; k++)
                r.m[i][j] += a.m[i][k] * b.m[k][j];
    return r;
}

Vec3 Apply(const Mat3& a, Vec3 v)
{
    return { a.m[0][0] * v.x + a.m[0][1] * v.y + a.m[0][2] * v.w,
             a.m[1][0] * v.x + a.m[1][1] * v.y + a.m[1][2] * v.w,
             a.m[2][0] * v.x + a.m[2][1] * v.y + a.m[2][2] * v.w };
}

Mat3 Rotate(float degrees)
{
    float t = degrees * 3.14159265f / 180.0f;
    return { { { std::cos(t), -std::sin(t), 0 }, { std::sin(t), std::cos(t), 0 }, { 0, 0, 1 } } };
}

Mat3 Transpose(const Mat3& a)
{
    Mat3 r;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            r.m[i][j] = a.m[j][i];
    return r;
}

float Round(float v)
{
    return std::round(v * 1000.0f) / 1000.0f + 0.0f;
}

void Print(const char* name, const Mat3& a)
{
    std::cout << name << ": [" << Round(a.m[0][0]) << ", " << Round(a.m[0][1]) << ", " << Round(a.m[0][2]) << "] ["
              << Round(a.m[1][0]) << ", " << Round(a.m[1][1]) << ", " << Round(a.m[1][2]) << "] ["
              << Round(a.m[2][0]) << ", " << Round(a.m[2][1]) << ", " << Round(a.m[2][2]) << "]" << std::endl;
}

int main()
{
    Mat3 T = { { { 1, 0, 3 }, { 0, 1, 2 }, { 0, 0, 1 } } };
    Mat3 R = Rotate(90);
    Mat3 M = Multiply(T, R);
    Print("M = T(3, 2) R(90)", M);

    Vec3 position = { 1, 0, 1 };
    Vec3 direction = { 1, 0, 0 };
    Vec3 p = Apply(M, position);
    Vec3 d = Apply(M, direction);
    std::cout << "position (1, 0, w = 1) -> (" << Round(p.x) << ", " << Round(p.y) << ", w = " << p.w << ")  rotated and moved" << std::endl;
    std::cout << "direction (1, 0, w = 0) -> (" << Round(d.x) << ", " << Round(d.y) << ", w = " << d.w << ")  rotated only" << std::endl;

    Print("R(30) R(30)^T", Multiply(Rotate(30), Transpose(Rotate(30))));
    Print("R(30)^T = R(-30)", Transpose(Rotate(30)));

    Mat3 S = { { { 2, 0, 0 }, { 0, 0.5f, 0 }, { 0, 0, 1 } } };
    Mat3 skew = Multiply(Rotate(45), Multiply(S, Rotate(-45)));
    Print("skew = R(45) S(2, 0.5) R(-45)", skew);
    Vec3 c = Apply(skew, { 1, 1, 1 });
    std::cout << "skew of (1, 1): (" << Round(c.x) << ", " << Round(c.y) << ")  along the 45 degree line: x2" << std::endl;
    return 0;
}
