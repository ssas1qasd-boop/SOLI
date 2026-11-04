#include <iostream>
#include <vector>

struct Vertex
{
    float x, y, z;
};

std::ostream& operator<<(std::ostream& stream, const Vertex& vertex)
{
    stream << vertex.x << ", " << vertex.y << ", " << vertex.z;
    return stream;
}

int main()
{
    std::vector<Vertex> vertices;
    vertices.push_back({ 1, 2, 3 });
    vertices.push_back({ 4, 5, 6 });

    for (const Vertex& v : vertices)
        std::cout << v << std::endl;

    vertices.erase(vertices.begin() + 1);
    std::cout << "After erase:" << std::endl;
    for (const Vertex& v : vertices)
        std::cout << v << std::endl;

    vertices.clear();
    std::cout << "Size after clear: " << vertices.size() << std::endl;
    std::cin.get();
}
