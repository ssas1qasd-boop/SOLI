#include <iostream>
#include <chrono>
#include <memory>

class Entity
{
public:
    Entity()
    {
        std::cout << "Created Entity" << std::endl;
    }

    ~Entity()
    {
        std::cout << "Destroyed Entity" << std::endl;
    }
};

class ScopedPtr
{
private:
    Entity* m_Ptr;

public:
    ScopedPtr(Entity* ptr)
        : m_Ptr(ptr)
    {
    }

    ~ScopedPtr()
    {
        delete m_Ptr;
    }
};

class Timer
{
private:
    const char* m_Name;
    std::chrono::steady_clock::time_point m_Start;

public:
    Timer(const char* name)
        : m_Name(name), m_Start(std::chrono::steady_clock::now())
    {
    }

    ~Timer()
    {
        auto end = std::chrono::steady_clock::now();
        long long ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - m_Start).count();
        std::cout << "Timer " << m_Name << ": " << (ns > 0 ? "more than 0" : "0") << " ns" << std::endl;
    }
};

int main()
{
    {
        ScopedPtr e = new Entity();
        std::cout << "inside the scope" << std::endl;
    }
    std::cout << "after the scope (ScopedPtr)" << std::endl;
    {
        std::unique_ptr<Entity> u = std::make_unique<Entity>();
        std::cout << "inside the scope" << std::endl;
    }
    std::cout << "after the scope (unique_ptr)" << std::endl;
    {
        Timer t("loop");
        long long sum = 0;
        for (int i = 0; i < 100; i++)
            sum += i;
        std::cout << "sum = " << sum << std::endl;
    }
    std::cout << "sizeof(Entity*) = " << sizeof(Entity*) << ", sizeof(ScopedPtr) = " << sizeof(ScopedPtr) << std::endl;
    return 0;
}
