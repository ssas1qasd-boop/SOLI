#include <iostream>
#include <vector>

struct Vertex
{
    float x, y, z;
};

std::ostream& operator<<(std::ostream& stream, const Vertex& vertex)
{
    stream << "(" << vertex.x << ", " << vertex.y << ", " << vertex.z << ")";
    return stream;
}

void Show(const std::vector<Vertex>& vertices)
{
    std::cout << "size " << vertices.size() << ":";
    for (const Vertex& v : vertices)
        std::cout << " " << v;
    std::cout << std::endl;
}

int main()
{
    Vertex fixed[5];
    std::cout << "Vertex fixed[5]: always " << sizeof(fixed) / sizeof(Vertex) << " vertices, " << sizeof(fixed) << " bytes" << std::endl;

    std::vector<Vertex> vertices;
    vertices.push_back({ 1, 2, 3 });
    vertices.push_back({ 4, 5, 6 });
    vertices.push_back({ 7, 8, 9 });
    Show(vertices);

    for (size_t i = 0; i < vertices.size(); i++)
        vertices[i].z = 0;
    Show(vertices);

    for (Vertex v : vertices)
        v.x = 100;
    std::cout << "after for (Vertex v ...) v.x = 100: first x = " << vertices[0].x << std::endl;
    for (Vertex& v : vertices)
        v.x = 100;
    std::cout << "after for (Vertex& v ...) v.x = 100: first x = " << vertices[0].x << std::endl;

    vertices.erase(vertices.begin() + 1);
    Show(vertices);
    std::cout << "&vertices[1] - &vertices[0] = " << (char*)&vertices[1] - (char*)&vertices[0] << " bytes (contiguous)" << std::endl;

    vertices.clear();
    Show(vertices);
    return 0;
}
