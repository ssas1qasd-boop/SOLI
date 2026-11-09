#include <iostream>
#include <vector>

int copies = 0;

struct Vertex
{
    float x, y, z;

    Vertex(float x, float y, float z)
        : x(x), y(y), z(z)
    {
    }

    Vertex(const Vertex& other)
        : x(other.x), y(other.y), z(other.z)
    {
        copies++;
    }
};

int main()
{
    std::vector<Vertex> plain;
    for (int i = 0; i < 3; i++)
    {
        plain.push_back(Vertex(1, 2, 3));
        std::cout << "push_back #" << i + 1 << ": capacity " << plain.capacity() << ", copies so far " << copies << std::endl;
    }
    std::cout << "push_back only:          " << copies << " copies" << std::endl;

    copies = 0;
    std::vector<Vertex> reserved;
    reserved.reserve(3);
    reserved.push_back(Vertex(1, 2, 3));
    reserved.push_back(Vertex(4, 5, 6));
    reserved.push_back(Vertex(7, 8, 9));
    std::cout << "reserve + push_back:     " << copies << " copies" << std::endl;

    copies = 0;
    std::vector<Vertex> emplaced;
    emplaced.reserve(3);
    emplaced.emplace_back(1, 2, 3);
    emplaced.emplace_back(4, 5, 6);
    emplaced.emplace_back(7, 8, 9);
    std::cout << "reserve + emplace_back:  " << copies << " copies" << std::endl;

    std::vector<int> grow;
    size_t last = 0;
    std::cout << "capacity steps for 100 push_backs:";
    for (int i = 0; i < 100; i++)
    {
        grow.push_back(i);
        if (grow.capacity() != last)
        {
            last = grow.capacity();
            std::cout << " " << last;
        }
    }
    std::cout << std::endl;
    return 0;
}
