#include <iostream>
#include <vector>
#include <cmath>

struct Vec3
{
    float x, y, z;
};

struct Plane
{
    Vec3 n;
    float d;
};

float Length(Vec3 a, Vec3 b)
{
    return std::sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y) + (a.z - b.z) * (a.z - b.z));
}

bool Inside(const std::vector<Plane>& solid, Vec3 p)
{
    for (const Plane& h : solid)
        if (h.n.x * p.x + h.n.y * p.y + h.n.z * p.z > h.d)
            return false;
    return true;
}

int main()
{
    std::vector<Vec3> v = { { -1, -1, -1 }, { 1, -1, -1 }, { 1, 1, -1 }, { -1, 1, -1 }, { -1, -1, 1 }, { 1, -1, 1 }, { 1, 1, 1 }, { -1, 1, 1 } };

    int edges[12][2] = { { 0, 1 }, { 1, 2 }, { 2, 3 }, { 3, 0 }, { 4, 5 }, { 5, 6 }, { 6, 7 }, { 7, 4 }, { 0, 4 }, { 1, 5 }, { 2, 6 }, { 3, 7 } };
    float wire = 0.0f;
    for (auto& e : edges)
        wire += Length(v[e[0]], v[e[1]]);
    std::cout << "wireframe: 12 edges, total length = " << wire << ", area = ?, volume = ?" << std::endl;

    int faces[6][4] = { { 0, 3, 2, 1 }, { 4, 5, 6, 7 }, { 0, 1, 5, 4 }, { 1, 2, 6, 5 }, { 2, 3, 7, 6 }, { 3, 0, 4, 7 } };
    float area = 0.0f;
    for (auto& f : faces)
        area += Length(v[f[0]], v[f[1]]) * Length(v[f[1]], v[f[2]]);
    std::cout << "surface: 6 faces, area = " << area << ", volume = ?" << std::endl;

    std::vector<Plane> solid = { { { 1, 0, 0 }, 1 }, { { -1, 0, 0 }, 1 }, { { 0, 1, 0 }, 1 }, { { 0, -1, 0 }, 1 }, { { 0, 0, 1 }, 1 }, { { 0, 0, -1 }, 1 } };
    std::cout << "solid: 6 half-spaces, (0, 0, 0) inside: " << Inside(solid, { 0, 0, 0 }) << ", (1.5, 0, 0) inside: " << Inside(solid, { 1.5f, 0, 0 }) << std::endl;
    int in = 0, cells = 0;
    for (float x = -1.5f; x <= 1.5f; x += 1.0f)
        for (float y = -1.5f; y <= 1.5f; y += 1.0f)
            for (float z = -1.5f; z <= 1.5f; z += 1.0f)
            {
                cells++;
                if (Inside(solid, { x, y, z }))
                    in++;
            }
    std::cout << "solid: " << in << " of " << cells << " unit cells inside -> volume = " << in * 1.0f << std::endl;
    return 0;
}
