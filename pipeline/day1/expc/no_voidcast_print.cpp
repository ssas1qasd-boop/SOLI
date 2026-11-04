#include <iostream>
#include <cstring>

int main()
{
    char* buffer = new char[8];
    memset(buffer, 0, 8);
    std::cout << "buffer = " << buffer << std::endl;
    for (int i = 0; i < 8; i++)
        std::cout << (int)buffer[i] << " ";
    std::cout << std::endl;
    delete[] buffer;
    std::cin.get();
}
