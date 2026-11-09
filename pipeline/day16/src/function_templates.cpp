#include <iostream>
#include <string>
#include <cstring>

template<typename T>
void Swap(T& a, T& b)
{
    T temp = a;
    a = b;
    b = temp;
}

template<typename T>
T Max(T a, T b)
{
    std::cout << "  [Max<T>] ";
    return a > b ? a : b;
}

template<>
const char* Max<const char*>(const char* a, const char* b)
{
    std::cout << "  [Max<const char*> special] ";
    return std::strcmp(a, b) > 0 ? a : b;
}

int Max(int a, int b)
{
    std::cout << "  [plain int Max] ";
    return a > b ? a : b;
}

template<typename A, typename B>
auto Add(A a, B b)
{
    return a + b;
}

int main()
{
    int x = 1, y = 2;
    Swap(x, y);
    std::cout << "Swap ints: x = " << x << ", y = " << y << std::endl;
    std::string s1 = "left", s2 = "right";
    Swap(s1, s2);
    std::cout << "Swap strings: s1 = " << s1 << ", s2 = " << s2 << std::endl;

    std::cout << Max(3, 9) << std::endl;
    std::cout << Max<int>(3, 9) << std::endl;
    std::cout << Max(2.5, 1.5) << std::endl;
    const char* a = "apple";
    const char* b = "banana";
    std::cout << Max(a, b) << std::endl;

    std::cout << "Add(2, 0.5) = " << Add(2, 0.5) << ", Add(1, 2) = " << Add(1, 2) << std::endl;
    std::cout << "sizeof(Add(2, 0.5)) = " << sizeof(Add(2, 0.5)) << ", sizeof(Add(1, 2)) = " << sizeof(Add(1, 2)) << std::endl;
    return 0;
}
