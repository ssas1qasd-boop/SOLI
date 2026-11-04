#include <iostream>
#include <vector>

struct Vertex
{
    float x, y, z;
};

int main()
{
    std::vector<Vertex> vertices = { { 1, 2, 3 }, { 4, 5, 6 } };

    for (size_t i = 0; i < vertices.size(); i++)
        std::cout << "index " << i << ": x = " << vertices[i].x << std::endl;

    for (const Vertex& v : vertices)
        std::cout << v.x << ", " << v.y << ", " << v.z << std::endl;

    for (Vertex& v : vertices)
        v.x = v.x * 10;

    std::cout << "after x * 10: " << vertices[0].x << " and " << vertices[1].x << std::endl;
    std::cin.get();
}
