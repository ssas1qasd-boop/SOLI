#include <iostream>

class Entity
{
private:
    int m_X = 0;
    mutable int m_DebugCount = 0;

public:
    int GetX() const
    {
        m_DebugCount++;
        return m_X;
    }

    void SetX(int x)
    {
        m_X = x;
    }

    int GetDebugCount() const
    {
        return m_DebugCount;
    }
};

void PrintEntity(const Entity& e)
{
    std::cout << "x = " << e.GetX() << std::endl;
}

int main()
{
    Entity e;
    e.SetX(7);
    PrintEntity(e);
    PrintEntity(e);
    std::cout << "GetX was called " << e.GetDebugCount() << " times" << std::endl;
    std::cin.get();
}
