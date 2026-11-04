#include <iostream>

struct Vector3
{
    float x, y, z;

    Vector3()
        : x(10), y(11), z(12)
    {
    }
};

long long Distance(const void* a, const void* b)
{
    return (long long)((const char*)a - (const char*)b);
}

int main()
{
    int value = 5;
    int array[5];
    for (int i = 0; i < 5; i++)
        array[i] = 2;
    Vector3 vector;

    int* hvalue = new int;
    *hvalue = 5;
    int* harray = new int[5];
    for (int i = 0; i < 5; i++)
        harray[i] = 2;
    Vector3* hvector = new Vector3();

    std::cout << "sizeof: int = " << sizeof(value) << ", int[5] = " << sizeof(array) << ", Vector3 = " << sizeof(vector) << std::endl;
    std::cout << "stack: &value = " << &value << ", array = " << array << ", &vector = " << &vector << std::endl;
    std::cout << "heap:  hvalue = " << hvalue << ", harray = " << harray << ", hvector = " << hvector << std::endl;
    std::cout << "stack gaps: &value - array = " << Distance(&value, array) << ", array - &vector = " << Distance(array, &vector) << " bytes" << std::endl;
    std::cout << "heap gaps: harray - hvalue = " << Distance(harray, hvalue) << ", hvector - harray = " << Distance(hvector, harray) << " bytes" << std::endl;
    std::cout << "same values: " << value << " = " << *hvalue << ", " << array[4] << " = " << harray[4] << ", " << vector.z << " = " << hvector->z << std::endl;

    delete hvalue;
    delete[] harray;
    delete hvector;
    return 0;
}
