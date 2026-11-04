#include <iostream>

struct NoInit
{
    float x, y;
};

class Entity
{
public:
    float x, y;

    Entity()
    {
        x = 0.0f;
        y = 0.0f;
        std::cout << "Entity() ran" << std::endl;
    }

    Entity(float x, float y)
    {
        this->x = x;
        this->y = y;
        std::cout << "Entity(float, float) ran" << std::endl;
    }

    void Print()
    {
        std::cout << x << ", " << y << std::endl;
    }
};

class Log
{
public:
    Log() = delete;

    static void Write(const char* message)
    {
        std::cout << "[Log] " << message << std::endl;
    }
};

int main()
{
    NoInit* first = new NoInit;
    first->x = 7.0f;
    first->y = 9.0f;
    delete first;

    NoInit* raw = new NoInit;
    std::cout << "no constructor: " << raw->x << ", " << raw->y << std::endl;
    delete raw;

    Entity e1;
    e1.Print();

    Entity e2(10.0f, 5.0f);
    e2.Print();

    Entity* e3 = new Entity(3.0f, 4.0f);
    e3->Print();
    delete e3;

    Log::Write("Hello");
    return 0;
}
