#include <iostream>

class Counter
{
private:
    int count;

public:
    void Reset()
    {
        count = 0;
    }

    void Add(int n)
    {
        if (n > 0)
            count += n;
    }

    int Get()
    {
        return count;
    }

    void Where()
    {
        std::cout << "inside Where(): this = " << this << std::endl;
    }
};

int main()
{
    Counter clicks;
    clicks.Reset();
    clicks.Add(3);
    clicks.Add(4);
    clicks.Add(-100);
    std::cout << "clicks.Get() = " << clicks.Get() << std::endl;

    std::cout << "&clicks = " << &clicks << std::endl;
    clicks.Where();

    Counter other;
    other.Reset();
    other.Add(1);
    std::cout << "other.Get() = " << other.Get() << "   clicks.Get() = " << clicks.Get() << std::endl;
    std::cout << "&other = " << &other << std::endl;
    other.Where();
    return 0;
}
