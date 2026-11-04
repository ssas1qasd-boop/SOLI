// Code from "POINTERS in C++" (The Cherno), with prints added so we can SEE what happens.
#include <iostream>
#include <cstring>

#define LOG(x) std::cout << x << std::endl

int main()
{
    std::cout << "=== Code 1: null pointer ===\n";
    void* p0 = nullptr;
    std::cout << "p0 = " << p0 << "   (0 = not a valid address)\n\n";

    std::cout << "=== Code 2: take an address with & ===\n";
    int var = 8;
    void* ptr = &var;
    std::cout << "var  = " << var << "\n";
    std::cout << "&var = " << &var << "\n";
    std::cout << "ptr  = " << ptr << "   (same number as &var)\n\n";

    std::cout << "=== Code 3: the type does not change the address ===\n";
    int* iptr = &var;
    double* dptr = (double*)&var;
    std::cout << "int*    -> " << iptr << "\n";
    std::cout << "double* -> " << dptr << "   (same address)\n";
    std::cout << "sizeof(int) = " << sizeof(int) << " bytes, sizeof(double) = " << sizeof(double) << " bytes\n\n";

    std::cout << "=== Code 4: dereference with * ===\n";
    std::cout << "before: var = " << var << "\n";
    *iptr = 10;
    std::cout << "after *ptr = 10: var = ";
    LOG(var);
    std::cout << "\n";

    std::cout << "=== Code 5: heap with new / delete ===\n";
    char* buffer = new char[8];
    memset(buffer, 0, 8);
    std::cout << "buffer points to " << (void*)buffer << "\n";
    std::cout << "bytes: ";
    for (int i = 0; i < 8; i++) std::cout << (int)buffer[i] << " ";
    std::cout << "\n\n";

    std::cout << "=== Code 6: pointer to pointer ===\n";
    char** pp = &buffer;
    std::cout << "pp        = " << (void*)pp << "   (address of buffer variable)\n";
    std::cout << "*pp       = " << (void*)*pp << "   (address of the 8 bytes)\n";
    std::cout << "(*pp)[0]  = " << (int)(*pp)[0] << "   (the data itself)\n\n";

    delete[] buffer;

    std::cout << "sizeof(void*) = " << sizeof(void*) << " bytes  (64-bit system)\n";
}
