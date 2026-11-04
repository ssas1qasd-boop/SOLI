#include <iostream>
#include <vector>
#include <set>
#include <utility>

struct Vec3
{
    float x, y, z;
};

struct Triangle
{
    unsigned int a, b, c;
};

float Area2(float ax, float ay, float bx, float by, float cx, float cy)
{
    return (bx - ax) * (cy - ay) - (cx - ax) * (by - ay);
}

void Barycentric(float px, float py)
{
    float x0 = 0, y0 = 0, x1 = 4, y1 = 0, x2 = 0, y2 = 4;
    float A = Area2(x0, y0, x1, y1, x2, y2);
    float alpha = Area2(px, py, x1, y1, x2, y2) / A;
    float beta = Area2(x0, y0, px, py, x2, y2) / A;
    float gamma = Area2(x0, y0, x1, y1, px, py) / A;
    int zeros = (alpha == 0) + (beta == 0) + (gamma == 0);
    const char* where = "inside";
    if (alpha < 0 || beta < 0 || gamma < 0)
        where = "outside";
    else if (zeros == 2)
        where = "on a vertex";
    else if (zeros == 1)
        where = "on an edge";
    std::cout << "P = (" << px << ", " << py << "): alpha = " << alpha << ", beta = " << beta << ", gamma = " << gamma
              << ", sum = " << alpha + beta + gamma << "  " << where << std::endl;
}

int main()
{
    std::vector<Vec3> vertices = { {0, 0, 0}, {1, 0, 0}, {1, 1, 0}, {0, 1, 0},
                                   {0, 0, 1}, {1, 0, 1}, {1, 1, 1}, {0, 1, 1} };
    std::vector<Triangle> triangles = { {0, 2, 1}, {0, 3, 2}, {4, 5, 6}, {4, 6, 7},
                                        {0, 1, 5}, {0, 5, 4}, {1, 2, 6}, {1, 6, 5},
                                        {2, 3, 7}, {2, 7, 6}, {3, 0, 4}, {3, 4, 7} };

    size_t faceList = triangles.size() * 3 * sizeof(Vec3);
    size_t indexed = vertices.size() * sizeof(Vec3) + triangles.size() * sizeof(Triangle);
    std::cout << "face list: " << triangles.size() * 3 << " corners x " << sizeof(Vec3) << " bytes = " << faceList << " bytes" << std::endl;
    std::cout << "indexed:   " << vertices.size() << " vertices x " << sizeof(Vec3) << " + "
              << triangles.size() << " triangles x " << sizeof(Triangle) << " = " << indexed << " bytes" << std::endl;

    std::set<std::pair<unsigned int, unsigned int>> edges;
    for (const Triangle& t : triangles)
    {
        unsigned int corner[3] = { t.a, t.b, t.c };
        for (int k = 0; k < 3; k++)
        {
            unsigned int p = corner[k], q = corner[(k + 1) % 3];
            edges.insert({ std::min(p, q), std::max(p, q) });
        }
    }
    int V = (int)vertices.size(), E = (int)edges.size(), F = (int)triangles.size();
    std::cout << "V = " << V << ", E = " << E << ", F = " << F << ", V - E + F = " << V - E + F << std::endl;

    Barycentric(1, 1);
    Barycentric(2, 2);
    Barycentric(4, 0);
    Barycentric(3, 3);
    return 0;
}
