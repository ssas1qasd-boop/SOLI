#include <iostream>
#include <string>

template<typename T>
void Print(T value)
{
    std::cout << value << "   <- made by the compiler as: " << __PRETTY_FUNCTION__ << std::endl;
}

template<typename T>
T Biggest(T a, T b)
{
    return a > b ? a : b;
}

template<typename T>
void NeverCalled(T value)
{
    value.ThisDoesNotExist();
}

int main()
{
    Print(5);
    Print(5.5f);
    Print("Hello");
    Print<std::string>("Hello");
    Print<int>(7.9);

    std::cout << "Biggest(3, 9) = " << Biggest(3, 9) << std::endl;
    std::cout << "Biggest(2.5, 1.5) = " << Biggest(2.5, 1.5) << std::endl;
    std::cout << "Biggest<std::string>(\"apple\", \"banana\") = " << Biggest<std::string>("apple", "banana") << std::endl;
    std::cout << "NeverCalled has a mistake inside, but nobody called it, so no error" << std::endl;
    return 0;
}
