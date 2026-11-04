#include <iostream>
#include <vector>
#include <string>
#include <cmath>

struct Vertex
{
    float x, y, z;
};

struct Edge
{
    std::string curve;
    int v0, v1;
};

struct Use
{
    int edge;
    bool reversed;
};

struct Loop
{
    std::vector<Use> uses;
};

struct Face
{
    std::string surface;
    std::vector<int> loops;
};

const float PI = 3.14159265f;
const float R = 1.0f;
const float H = 2.0f;

Vertex Circle(float t, float z)
{
    return { R * std::cos(t), R * std::sin(t), z };
}

Vertex Side(float u, float v)
{
    return { R * std::cos(u), R * std::sin(u), v };
}

int main()
{
    std::vector<Vertex> vertices = { { R, 0.0f, H }, { R, 0.0f, 0.0f } };

    std::vector<Edge> edges = {
        { "circle z = 2", 0, 0 },
        { "line (seam)", 0, 1 },
        { "circle z = 0", 1, 1 }
    };

    std::vector<Loop> loops = {
        { { { 0, false } } },
        { { { 0, true }, { 1, false }, { 2, false }, { 1, true } } },
        { { { 2, true } } }
    };

    std::vector<Face> faces = {
        { "plane z = 2 (top)", { 0 } },
        { "cylinder r = 1 (side)", { 1 } },
        { "plane z = 0 (bottom)", { 2 } }
    };

    std::cout << "V = " << vertices.size() << ", E = " << edges.size() << ", F = " << faces.size() << std::endl;
    for (int i = 0; i < (int)edges.size(); i++)
        std::cout << "edge " << i << ": " << edges[i].curve << ", from v" << edges[i].v0 << " to v" << edges[i].v1 << std::endl;

    for (int f = 0; f < (int)faces.size(); f++)
    {
        std::cout << "face " << f << ": " << faces[f].surface << ", loop:";
        for (int l : faces[f].loops)
            for (Use u : loops[l].uses)
                std::cout << " e" << u.edge << (u.reversed ? "-" : "+");
        std::cout << std::endl;
    }

    std::vector<int> count(edges.size(), 0);
    for (Loop& loop : loops)
        for (Use u : loop.uses)
            count[u.edge]++;
    for (int i = 0; i < (int)edges.size(); i++)
        std::cout << "edge " << i << " is used " << count[i] << " times" << (count[i] == 2 ? "  (ok: manifold)" : "  (NOT manifold)") << std::endl;

    int euler = (int)vertices.size() - (int)edges.size() + (int)faces.size();
    std::cout << "V - E + F = " << euler << std::endl;

    Vertex a = Circle(PI / 2.0f, H);
    Vertex b = Side(PI / 2.0f, 1.0f);
    std::cout << "C(t = pi/2) on edge 0 = (" << a.x << ", " << a.y << ", " << a.z << ")" << std::endl;
    std::cout << "S(u = pi/2, v = 1) on face 1 = (" << b.x << ", " << b.y << ", " << b.z << ")" << std::endl;
    return 0;
}
