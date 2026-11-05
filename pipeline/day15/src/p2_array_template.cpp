#include <iostream>
#include <string>
#include <array>

template<typename T, int N>
class Array
{
private:
    T m_Data[N];

public:
    int GetSize() const
    {
        return N;
    }

    T& operator[](int index)
    {
        return m_Data[index];
    }
};

int main()
{
    Array<int, 5> numbers;
    for (int i = 0; i < numbers.GetSize(); i++)
        numbers[i] = i * 10;
    std::cout << "Array<int, 5>: size " << numbers.GetSize() << ", sizeof " << sizeof(numbers) << " bytes, numbers[4] = " << numbers[4] << std::endl;

    Array<float, 3> position;
    position[0] = 1.5f;
    std::cout << "Array<float, 3>: size " << position.GetSize() << ", sizeof " << sizeof(position) << " bytes" << std::endl;

    Array<std::string, 2> names;
    names[0] = "Cherno";
    names[1] = "Cem";
    std::cout << "Array<std::string, 2>: sizeof " << sizeof(names) << " bytes, names[1] = " << names[1] << std::endl;

    std::array<int, 5> standard = { 0, 10, 20, 30, 40 };
    std::cout << "std::array<int, 5>: size " << standard.size() << ", sizeof " << sizeof(standard) << " bytes" << std::endl;
    return 0;
}
