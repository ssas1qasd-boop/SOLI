#include <iostream>

int s_Variable = 10;

void Function()
{
    std::cout << "Function from main.cpp" << std::endl;
}

void PrintStatic();

int main()
{
    std::cout << "main.cpp sees:   " << s_Variable << std::endl;
    Function();
    PrintStatic();
    std::cin.get();
}
