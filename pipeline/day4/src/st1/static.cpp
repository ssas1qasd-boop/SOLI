#include <iostream>

static int s_Variable = 5;

static void Function()
{
    std::cout << "Function from static.cpp" << std::endl;
}

void PrintStatic()
{
    std::cout << "static.cpp sees: " << s_Variable << std::endl;
    Function();
}
