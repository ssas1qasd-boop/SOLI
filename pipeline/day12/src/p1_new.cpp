#include <iostream>
#include <string>
#include <cstdlib>

size_t lastSize = 0;

void* operator new(size_t size)
{
    lastSize = size;
    return malloc(size);
}

void* operator new[](size_t size)
{
    lastSize = size;
    return malloc(size);
}

void operator delete(void* memory) noexcept
{
    free(memory);
}

void operator delete[](void* memory) noexcept
{
    free(memory);
}

class Entity
{
public:
    std::string name;

    Entity()
        : name("Unknown")
    {
        std::cout << "Entity() ran" << std::endl;
    }
};

int main()
{
    int* b = new int;
    std::cout << "new int: " << lastSize << " bytes" << std::endl;
    int* arr = new int[50];
    std::cout << "new int[50]: " << lastSize << " bytes" << std::endl;

    Entity* e = new Entity();
    std::cout << "new Entity(): " << lastSize << " bytes, name = " << e->name << std::endl;
    Entity* entities = new Entity[3];
    std::cout << "new Entity[3]: " << lastSize << " bytes (sizeof(Entity) = " << sizeof(Entity) << ")" << std::endl;

    Entity* m = (Entity*)malloc(sizeof(Entity));
    std::cout << "malloc(sizeof(Entity)): no \"Entity() ran\" above this line" << std::endl;

    delete b;
    delete[] arr;
    delete e;
    delete[] entities;
    free(m);
    return 0;
}
