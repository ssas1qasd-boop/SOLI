#include <iostream>
#include <string>

class Entity
{
public:
    std::string name;

    Entity(const std::string& n)
        : name(n)
    {
        std::cout << "Created Entity " << name << std::endl;
    }

    ~Entity()
    {
        std::cout << "Destroyed Entity " << name << std::endl;
    }
};

int* CreateArray()
{
    int* array = new int[50];
    array[0] = 7;
    return array;
}

void FillArray(int* array)
{
    array[0] = 9;
}

int main()
{
    std::cout << "main starts" << std::endl;
    Entity a("a");
    {
        Entity b("b");
        std::cout << "end of the empty scope" << std::endl;
    }
    if (true)
    {
        Entity c("c");
    }
    for (int i = 0; i < 2; i++)
    {
        Entity d("d" + std::to_string(i));
    }
    {
        Entity* h = new Entity("heap");
        std::cout << "end of the scope with new: " << h->name << " is still alive" << std::endl;
    }
    int* fromHeap = CreateArray();
    std::cout << "CreateArray (heap): array[0] = " << fromHeap[0] << std::endl;
    delete[] fromHeap;
    int array[50];
    FillArray(array);
    std::cout << "FillArray (array made in main): array[0] = " << array[0] << std::endl;
    std::cout << "main ends" << std::endl;
    return 0;
}
