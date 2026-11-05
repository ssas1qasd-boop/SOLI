#include <iostream>
#include <cmath>

const float PI = 3.14159265f;

struct Range
{
    float from, to;
};

struct Point
{
    float x, y, z;
};

Point At(float r, float t, float h)
{
    return { r * std::sin(t), r * std::cos(t), h };
}

float Value(Range v, int i, int n)
{
    if (v.to == v.from)
        return v.from;
    return v.from + (v.to - v.from) * i / (n - 1);
}

void Shape(const char* name, Range R, Range T, Range H)
{
    int params = (R.to > R.from) + (T.to > T.from) + (H.to > H.from);
    const char* kind[] = { "point", "curve", "surface", "solid" };
    int n = 3, count = 0;
    float rMax = 0.0f, zMax = 0.0f;
    for (int i = 0; i < (R.to > R.from ? n : 1); i++)
        for (int j = 0; j < (T.to > T.from ? n : 1); j++)
            for (int k = 0; k < (H.to > H.from ? n : 1); k++)
            {
                Point p = At(Value(R, i, n), Value(T, j, n), Value(H, k, n));
                rMax = std::fmax(rMax, std::sqrt(p.x * p.x + p.y * p.y));
                zMax = std::fmax(zMax, p.z);
                count++;
            }
    std::cout << name << ": " << params << " free -> " << kind[params] << ", " << count << " sample points, max r = " << rMax << ", max z = " << zMax << std::endl;
}

int main()
{
    Point p = At(10.0f, PI, 25.0f);
    std::cout << "R = 10, theta = pi, H = 25 -> (" << p.x << ", " << p.y << ", " << p.z << ")" << std::endl;
    Shape("point     ", { 10, 10 }, { PI, PI }, { 25, 25 });
    Shape("circle    ", { 10, 10 }, { -PI, PI }, { 0, 0 });
    Shape("cylinder  ", { 10, 10 }, { -PI, PI }, { 0, 25 });
    Shape("disk      ", { 0, 10 }, { -PI, PI }, { 0, 0 });
    Shape("solid cyl.", { 0, 10 }, { -PI, PI }, { 0, 25 });
    Shape("hollow    ", { 5, 10 }, { -PI, PI }, { 0, 25 });
    std::cout << "areas / volumes: cylinder 2 pi R H = " << 2 * PI * 10 * 25 << ", disk pi R^2 = " << PI * 100 << std::endl;
    std::cout << "solid pi R^2 H = " << PI * 100 * 25 << ", hollow pi (10^2 - 5^2) H = " << PI * 75 * 25 << std::endl;
    return 0;
}
