#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <memory>
#include <utility>

struct Resource
{
    std::string Name;
    Resource(const std::string& name) : Name(name) { std::cout << "  acquire " << Name << std::endl; }
    ~Resource() { std::cout << "  release " << Name << std::endl; }
};

constexpr int Square(int x)
{
    return x * x;
}

template<typename T>
void SortAndPrint(std::vector<T> items)
{
    std::sort(items.begin(), items.end());
    for (const T& item : items)
        std::cout << item << " ";
    std::cout << std::endl;
}

int main()
{
    std::cout << "RAII:" << std::endl;
    {
        Resource file("file");
        std::unique_ptr<Resource> texture = std::make_unique<Resource>("texture");
        std::cout << "  leaving the scope" << std::endl;
    }

    std::string big(1000, 'x');
    const char* before = big.data();
    std::string moved = std::move(big);
    std::cout << "move: same buffer? " << (moved.data() == before ? "yes" : "no") << ", old size now " << big.size() << ", new size " << moved.size() << std::endl;

    static_assert(Square(12) == 144, "computed while compiling");
    constexpr int area = Square(12);
    std::cout << "constexpr Square(12) = " << area << " (checked by static_assert at compile time)" << std::endl;

    std::cout << "one template, two types: ";
    SortAndPrint<int>({ 5, 2, 9, 1 });
    std::cout << "                         ";
    SortAndPrint<std::string>({ "map", "auto", "vector", "glm" });
    return 0;
}
