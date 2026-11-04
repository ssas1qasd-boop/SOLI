#include <iostream>
#include <vector>

struct Vertex
{
    float x, y, z;
};

int main()
{
    std::vector<Vertex> vertices;
    std::cout << "size at start: " << vertices.size() << std::endl;

    vertices.push_back({ 1, 2, 3 });
    vertices.push_back({ 4, 5, 6 });
    Vertex v = { 7, 8, 9 };
    vertices.push_back(v);

    std::cout << "size now: " << vertices.size() << std::endl;
    std::cout << "vertices[0].x = " << vertices[0].x << std::endl;
    std::cout << "vertices.at(1).y = " << vertices.at(1).y << std::endl;
    std::cin.get();
}
