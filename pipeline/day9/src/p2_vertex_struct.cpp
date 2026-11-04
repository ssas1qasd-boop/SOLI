#include <iostream>
#include <cstddef>

struct Vertex
{
    float x, y;
    float u, v;
};

int main()
{
    Vertex square[4] = {
        { -0.5f, -0.5f, 0.0f, 0.0f },
        {  0.5f, -0.5f, 1.0f, 0.0f },
        {  0.5f,  0.5f, 1.0f, 1.0f },
        { -0.5f,  0.5f, 0.0f, 1.0f }
    };

    std::cout << "sizeof(Vertex) = " << sizeof(Vertex) << " bytes  (the stride)" << std::endl;
    std::cout << "offsetof(Vertex, x) = " << offsetof(Vertex, x) << std::endl;
    std::cout << "offsetof(Vertex, u) = " << offsetof(Vertex, u) << "  (where the texture coordinates start)" << std::endl;
    std::cout << "sizeof(square) = " << sizeof(square) << " bytes  (what glBufferData copies)" << std::endl;

    float* numbers = &square[0].x;
    std::cout << "the same bytes read as floats:";
    for (int i = 0; i < 16; i++)
        std::cout << " " << numbers[i];
    std::cout << std::endl;

    square[2].u = 2.0f;
    std::cout << "after square[2].u = 2: numbers[10] = " << numbers[10] << std::endl;
    return 0;
}
