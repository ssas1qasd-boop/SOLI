#include <iostream>
#include <cstring>

int main()
{
    char* buffer = new char[8];
    memset(buffer, 0, 8);
    char** ptr = &buffer;
    std::cout << "ptr      = " << (void*)ptr << std::endl;
    std::cout << "&buffer  = " << (void*)&buffer << std::endl;
    std::cout << "*ptr     = " << (void*)*ptr << std::endl;
    std::cout << "buffer   = " << (void*)buffer << std::endl;
    std::cout << "(*ptr)[0] = " << (int)(*ptr)[0] << std::endl;
    delete[] buffer;
    std::cin.get();
}
