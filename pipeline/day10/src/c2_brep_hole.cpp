#include <iostream>
#include <vector>
#include <map>
#include <utility>
#include <algorithm>

struct Face
{
    std::vector<std::vector<int>> loops;
};

struct Shape
{
    int V;
    std::vector<Face> faces;
};

std::map<std::pair<int, int>, int> CountEdges(const Shape& s)
{
    std::map<std::pair<int, int>, int> uses;
    for (const Face& f : s.faces)
        for (const std::vector<int>& loop : f.loops)
            for (int i = 0; i < (int)loop.size(); i++)
            {
                int a = loop[i];
                int b = loop[(i + 1) % loop.size()];
                uses[{ std::min(a, b), std::max(a, b) }]++;
            }
    return uses;
}

void Report(const char* name, const Shape& s)
{
    std::map<std::pair<int, int>, int> uses = CountEdges(s);
    int L = 0;
    for (const Face& f : s.faces)
        L += f.loops.size();
    int V = s.V, E = uses.size(), F = s.faces.size();
    std::cout << name << ": V = " << V << ", E = " << E << ", F = " << F << ", loops = " << L << std::endl;
    std::cout << "  V - E + F = " << V - E + F << ",  V - E + F - (loops - F) = " << V - E + F - (L - F) << std::endl;

    bool manifold = true;
    for (auto& [edge, n] : uses)
        if (n != 2)
        {
            manifold = false;
            std::cout << "  edge " << edge.first << "-" << edge.second << " is used by " << n << " faces" << std::endl;
        }
    std::cout << "  manifold: " << (manifold ? "yes" : "no") << std::endl;
}

int main()
{
    Shape box;
    box.V = 16;
    box.faces = {
        { { { 0, 3, 2, 1 }, { 8, 9, 10, 11 } } },
        { { { 4, 5, 6, 7 }, { 12, 15, 14, 13 } } },
        { { { 0, 1, 5, 4 } } },
        { { { 1, 2, 6, 5 } } },
        { { { 2, 3, 7, 6 } } },
        { { { 3, 0, 4, 7 } } },
        { { { 8, 12, 13, 9 } } },
        { { { 9, 13, 14, 10 } } },
        { { { 10, 14, 15, 11 } } },
        { { { 11, 15, 12, 8 } } }
    };
    Report("box with a hole", box);

    Shape cubes;
    cubes.V = 14;
    cubes.faces = {
        { { { 0, 3, 2, 1 } } },
        { { { 4, 5, 6, 7 } } },
        { { { 0, 1, 5, 4 } } },
        { { { 1, 2, 6, 5 } } },
        { { { 2, 3, 7, 6 } } },
        { { { 3, 0, 4, 7 } } },
        { { { 2, 10, 9, 8 } } },
        { { { 6, 11, 12, 13 } } },
        { { { 2, 8, 11, 6 } } },
        { { { 8, 9, 12, 11 } } },
        { { { 9, 10, 13, 12 } } },
        { { { 10, 2, 6, 13 } } }
    };
    Report("two cubes touching at one edge", cubes);
    return 0;
}
