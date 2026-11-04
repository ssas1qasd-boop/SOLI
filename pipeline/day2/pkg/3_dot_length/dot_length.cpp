#include <iostream>
#include <cmath>

float dot(const float* a, const float* b, int n)
{
    float sum = 0.0f;
    for (int i = 0; i < n; i++)
        sum += a[i] * b[i];
    return sum;
}

float length(const float* a, int n)
{
    return std::sqrt(dot(a, a, n));
}

int main()
{
    float a[] = { 2, 5 };
    float b[] = { 7, 1 };
    std::cout << "[2,5] . [7,1] = " << dot(a, b, 2) << std::endl;

    float c[] = { 1, 2, 3 };
    float d[] = { -2, 0, 5 };
    std::cout << "[1,2,3] . [-2,0,5] = " << dot(c, d, 3) << std::endl;

    std::cout << "[2,5] . [2,5] = " << dot(a, a, 2) << std::endl;
    std::cout << "length of [2,5] = " << length(a, 2) << std::endl;
    std::cout << "sqrt(29) = " << std::sqrt(29.0f) << std::endl;
    std::cin.get();
}
