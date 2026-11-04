#include <iostream>

class Entity
{
public:
    float x, y;

    Entity()
    {
        x = 0.0f;
        y = 0.0f;
        std::cout << "Created Entity!" << std::endl;
    }

    ~Entity()
    {
        std::cout << "Destroyed Entity!" << std::endl;
    }
};

class Buffer
{
public:
    int size;
    float* data;

    Buffer(int n)
    {
        size = n;
        data = new float[n];
        std::cout << "Buffer(" << n << "): new float[" << n << "]" << std::endl;
    }

    ~Buffer()
    {
        delete[] data;
        std::cout << "~Buffer(): delete[] " << size << " floats" << std::endl;
    }
};

void Function()
{
    std::cout << "Function start" << std::endl;
    Entity e;
    std::cout << "Function end" << std::endl;
}

int main()
{
    Function();
    std::cout << "back in main" << std::endl;

    Entity* heap = new Entity();
    std::cout << "heap Entity still alive" << std::endl;
    delete heap;

    {
        Buffer b(16);
        b.data[0] = 1.5f;
        std::cout << "inside the { }: data[0] = " << b.data[0] << std::endl;
    }
    std::cout << "after the { }" << std::endl;
    return 0;
}
