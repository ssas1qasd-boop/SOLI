#include <iostream>
#include <utility>
#include <vector>

template<typename T, int N>
struct Vec
{
    T v[N];

    Vec operator+(const Vec& other) const
    {
        Vec r;
        for (int i = 0; i < N; i++)
            r.v[i] = v[i] + other.v[i];
        return r;
    }

    T Dot(const Vec& other) const
    {
        T sum = 0;
        for (int i = 0; i < N; i++)
            sum += v[i] * other.v[i];
        return sum;
    }
};

template<typename T, int N>
void Print(const char* name, const Vec<T, N>& a)
{
    std::cout << name << " = (";
    for (int i = 0; i < N; i++)
        std::cout << a.v[i] << (i + 1 < N ? ", " : ")");
    std::cout << "  " << N << " x " << sizeof(T) << " bytes = " << sizeof(a) << std::endl;
}

int main()
{
    Vec<float, 3> a = { { 1.0f, 2.0f, 3.0f } };
    Vec<float, 3> b = { { 4.0f, 5.0f, 6.0f } };
    Print("a + b", a + b);
    std::cout << "a . b = " << a.Dot(b) << std::endl;

    Vec<int, 2> p = { { 3, 4 } };
    Print("p (int, 2)", p);
    std::cout << "p . p = " << p.Dot(p) << std::endl;

    std::pair pair(1, 2.5);
    std::vector list = { 1, 2, 3 };
    std::cout << "std::pair pair(1, 2.5): second = " << pair.second << ", std::vector list = {1, 2, 3}: size " << list.size() << std::endl;
    return 0;
}
