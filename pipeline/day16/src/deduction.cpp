#include <iostream>
#include <cstddef>

template<typename T, std::size_t N>
std::size_t Count(T (&array)[N])
{
    return N;
}

template<typename T, std::size_t N>
T Sum(const T (&array)[N])
{
    T total = 0;
    for (std::size_t i = 0; i < N; i++)
        total += array[i];
    return total;
}

template<typename T>
void Show(const T& value)
{
    std::cout << value << " (" << sizeof(T) << " bytes)" << std::endl;
}

int main()
{
    int numbers[5] = { 4, 8, 15, 16, 23 };
    float halves[3] = { 0.5f, 1.5f, 2.5f };
    std::cout << "Count(numbers) = " << Count(numbers) << ", Sum = " << Sum(numbers) << std::endl;
    std::cout << "Count(halves) = " << Count(halves) << ", Sum = " << Sum(halves) << std::endl;

    Show(42);
    Show(3.5);
    Show('A');
    Show<long long>(42);
    return 0;
}
