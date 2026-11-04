#include <iostream>
#include <vector>

int main()
{
    std::vector<int> numbers;
    const int* lastAddress = nullptr;

    for (int i = 1; i <= 9; i++)
    {
        numbers.push_back(i);
        const int* address = numbers.data();
        std::cout << "size " << numbers.size() << "  capacity " << numbers.capacity();
        if (address != lastAddress)
            std::cout << "   <- moved to a new place";
        std::cout << std::endl;
        lastAddress = address;
    }
    std::cin.get();
}
