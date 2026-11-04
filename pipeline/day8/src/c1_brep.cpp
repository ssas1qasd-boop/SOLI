#include <iostream>
#include <vector>
#include <string>

class Vertex
{
public:
    float x, y, z;
};

class Edge
{
public:
    int v0, v1;
};

class Face
{
public:
    std::vector<int> edges;
};

class Body
{
public:
    std::string name;
    std::vector<Vertex> vertices;
    std::vector<Edge> edges;
    std::vector<Face> faces;

    int Euler()
    {
        return (int)faces.size() - (int)edges.size() + (int)vertices.size();
    }

    int OpenEdges()
    {
        std::vector<int> used(edges.size(), 0);
        for (const Face& f : faces)
            for (int e : f.edges)
                used[e]++;
        int open = 0;
        for (int count : used)
            if (count != 2)
                open++;
        return open;
    }

    void Report()
    {
        std::cout << name << ": V = " << vertices.size() << ", E = " << edges.size()
                  << ", F = " << faces.size() << "  ->  F - E + V = " << Euler()
                  << ", edges not shared by 2 faces = " << OpenEdges() << std::endl;
    }
};

int main()
{
    Body cube;
    cube.name = "cube";
    cube.vertices = { {0, 0, 0}, {1, 0, 0}, {1, 1, 0}, {0, 1, 0},
                      {0, 0, 1}, {1, 0, 1}, {1, 1, 1}, {0, 1, 1} };
    cube.edges = { {0, 1}, {1, 2}, {2, 3}, {3, 0},
                   {4, 5}, {5, 6}, {6, 7}, {7, 4},
                   {0, 4}, {1, 5}, {2, 6}, {3, 7} };
    cube.faces = { {{0, 1, 2, 3}}, {{4, 5, 6, 7}}, {{0, 9, 4, 8}},
                   {{1, 10, 5, 9}}, {{2, 11, 6, 10}}, {{3, 8, 7, 11}} };
    cube.Report();

    Body pyramid;
    pyramid.name = "pyramid";
    pyramid.vertices = { {0, 0, 0}, {1, 0, 0}, {1, 1, 0}, {0, 1, 0}, {0.5f, 0.5f, 1} };
    pyramid.edges = { {0, 1}, {1, 2}, {2, 3}, {3, 0},
                      {0, 4}, {1, 4}, {2, 4}, {3, 4} };
    pyramid.faces = { {{0, 1, 2, 3}}, {{0, 5, 4}}, {{1, 6, 5}}, {{2, 7, 6}}, {{3, 4, 7}} };
    pyramid.Report();

    Body open = cube;
    open.name = "cube without its top face";
    open.faces.erase(open.faces.begin() + 1);
    open.Report();

    Face& front = cube.faces[2];
    std::cout << "front face of the cube uses edges:";
    for (int e : front.edges)
        std::cout << " " << e << "(" << cube.edges[e].v0 << "-" << cube.edges[e].v1 << ")";
    std::cout << std::endl;
    return 0;
}
