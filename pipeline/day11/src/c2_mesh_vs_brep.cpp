#include <iostream>
#include <cmath>
#include <vector>
#include <set>
#include <algorithm>

const float PI = 3.14159265f;
const float R = 1.0f;
const float H = 2.0f;

struct Mesh
{
    std::vector<float> xyz;
    std::vector<int> tris;
};

Mesh Cylinder(int n)
{
    Mesh m;
    for (int z = 0; z < 2; z++)
        for (int i = 0; i < n; i++)
        {
            float t = 2.0f * PI * i / n;
            m.xyz.insert(m.xyz.end(), { R * std::cos(t), R * std::sin(t), z * H });
        }
    for (int i = 0; i < n; i++)
    {
        int j = (i + 1) % n;
        m.tris.insert(m.tris.end(), { i, j, n + j, i, n + j, n + i });
    }
    for (int i = 1; i < n - 1; i++)
    {
        m.tris.insert(m.tris.end(), { 0, i + 1, i });
        m.tris.insert(m.tris.end(), { n, n + i, n + i + 1 });
    }
    return m;
}

int main()
{
    Mesh m = Cylinder(8);
    std::set<std::pair<int, int>> edges;
    for (int t = 0; t < (int)m.tris.size(); t += 3)
        for (int k = 0; k < 3; k++)
        {
            int a = m.tris[t + k], b = m.tris[t + (k + 1) % 3];
            edges.insert({ std::min(a, b), std::max(a, b) });
        }
    int V = m.xyz.size() / 3, E = edges.size(), F = m.tris.size() / 3;
    std::cout << "mesh, n = 8: V = " << V << ", E = " << E << ", F = " << F << ", V - E + F = " << V - E + F << std::endl;
    std::cout << "B-Rep (yesterday): V = 2, E = 3, F = 3, exact circle" << std::endl;

    std::cout << "n      triangles  bytes    max error" << std::endl;
    for (int n = 8; n <= 1024; n *= 4)
    {
        int tris = 4 * n - 4;
        int bytes = 2 * n * 3 * 4 + tris * 3 * 4;
        float error = R * (1.0f - std::cos(PI / n));
        std::cout << n << "\t" << tris << "\t   " << bytes << "\t    " << error << std::endl;
    }

    float tolerance = 0.01f;
    float radius = 50.0f;
    int n = 8;
    while (radius * (1.0f - std::cos(PI / n)) > tolerance)
        n *= 2;
    std::cout << "R = 50 mm, tolerance 0.01 mm: n = " << n << " (" << 4 * n - 4 << " triangles)" << std::endl;
    return 0;
}
