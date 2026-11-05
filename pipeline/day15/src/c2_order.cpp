#include <iostream>
#include <cmath>

struct Mat4
{
    float m[4][4];
};

Mat4 Multiply(const Mat4& a, const Mat4& b)
{
    Mat4 r = {};
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            for (int k = 0; k < 4; k++)
                r.m[i][j] += a.m[i][k] * b.m[k][j];
    return r;
}

Mat4 Translate(float tx, float ty, float tz)
{
    return { { { 1, 0, 0, tx }, { 0, 1, 0, ty }, { 0, 0, 1, tz }, { 0, 0, 0, 1 } } };
}

Mat4 RotateZ(float degrees)
{
    float t = degrees * 3.14159265f / 180.0f;
    float c = std::round(std::cos(t) * 1000) / 1000, s = std::round(std::sin(t) * 1000) / 1000;
    return { { { c, -s, 0, 0 }, { s, c, 0, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 1 } } };
}

void Where(const char* name, const Mat4& M)
{
    float cx = M.m[0][3], cy = M.m[1][3];
    float tipX = M.m[0][0] * 1 + M.m[0][3], tipY = M.m[1][0] * 1 + M.m[1][3];
    std::cout << name << ": center (" << cx + 0.0f << ", " << cy + 0.0f << "), nose (" << tipX + 0.0f << ", " << tipY + 0.0f << ")" << std::endl;
}

int main()
{
    Mat4 T = Translate(7.0f, 0.0f, 0.0f);
    for (int angle = 0; angle < 360; angle += 90)
    {
        Mat4 R = RotateZ((float)angle);
        std::cout << "angle " << angle << std::endl;
        Where("  T * R (spin in place)", Multiply(T, R));
        Where("  R * T (orbit around 0)", Multiply(R, T));
    }
    return 0;
}
