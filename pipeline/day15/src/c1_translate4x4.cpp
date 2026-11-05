#include <iostream>

struct Vec4
{
    float x, y, z, w;
};

struct Mat4
{
    float m[4][4];
};

Vec4 Apply(const Mat4& a, Vec4 v)
{
    float in[4] = { v.x, v.y, v.z, v.w };
    float out[4] = { 0, 0, 0, 0 };
    for (int i = 0; i < 4; i++)
        for (int k = 0; k < 4; k++)
            out[i] += a.m[i][k] * in[k];
    return { out[0], out[1], out[2], out[3] };
}

Mat4 Translate(float tx, float ty, float tz)
{
    return { { { 1, 0, 0, tx }, { 0, 1, 0, ty }, { 0, 0, 1, tz }, { 0, 0, 0, 1 } } };
}

void Print(const char* name, Vec4 v)
{
    std::cout << name << " (" << v.x << ", " << v.y << ", " << v.z << ", w = " << v.w << ")" << std::endl;
}

int main()
{
    Mat4 T = Translate(7.0f, 3.0f, 5.0f);
    std::cout << "T = translate(7, 3, 5):" << std::endl;
    for (int i = 0; i < 4; i++)
        std::cout << "  [" << T.m[i][0] << ", " << T.m[i][1] << ", " << T.m[i][2] << ", " << T.m[i][3] << "]" << std::endl;

    Vec4 vertex = { 1.0f, -1.0f, 2.0f, 1.0f };
    Print("vertex", vertex);
    Print("T * vertex", Apply(T, vertex));

    Vec4 normal = { 0.0f, 0.0f, 1.0f, 0.0f };
    Print("normal", normal);
    Print("T * normal", Apply(T, normal));

    Vec4 wrong = { 0.0f, 0.0f, 1.0f, 1.0f };
    Print("normal with w = 1 (wrong)", Apply(T, wrong));

    for (int frame = 0; frame <= 4; frame++)
    {
        float percentage = frame / 4.0f;
        Vec4 p = Apply(Translate(7.0f * percentage, 3.0f * percentage, 5.0f * percentage), vertex);
        std::cout << "frame " << frame << " (" << percentage * 100 << "%): (" << p.x << ", " << p.y << ", " << p.z << ")" << std::endl;
    }
    return 0;
}
