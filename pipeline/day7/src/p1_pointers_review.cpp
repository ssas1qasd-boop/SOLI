#include <iostream>
#include <cstring>

int main()
{
    int var = 8;
    void* ptr = &var;
    std::cout << "var = " << var << "   &var = " << &var << "   ptr = " << ptr << std::endl;

    int* intPtr = &var;
    *intPtr = 10;
    std::cout << "after *intPtr = 10: var = " << var << std::endl;

    std::cout << "sizeof(int*) = " << sizeof(int*) << "   sizeof(double*) = " << sizeof(double*)
              << "   sizeof(char*) = " << sizeof(char*) << std::endl;

    char* buffer = new char[8];
    memset(buffer, 0, 8);
    buffer[0] = 'H';
    *(buffer + 1) = 'i';
    std::cout << "buffer = " << (void*)buffer << "   text = " << buffer << std::endl;

    char** ptrToBuffer = &buffer;
    std::cout << "ptrToBuffer = " << ptrToBuffer << "   *ptrToBuffer = " << (void*)*ptrToBuffer
              << "   **ptrToBuffer = " << **ptrToBuffer << std::endl;

    delete[] buffer;
    buffer = nullptr;
    std::cout << "after delete[]: buffer = " << (void*)buffer << std::endl;
    return 0;
}
