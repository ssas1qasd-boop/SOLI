#include <iostream>
#include <glm/glm.hpp>

float dot(const float* v, const float* w, int n)
{
    float sum = 0.0f;
    for (int i = 0; i < n; i++)
        sum += v[i] * w[i];
    return sum;
}

int main()
{
    float a[] = { 1, 2 };
    float b[] = { 3, 4 };
    std::cout << "[1,2] . [3,4] = " << dot(a, b, 2) << std::endl;

    float c[] = { 6, 2, 8, 3 };
    float d[] = { 1, 8, 5, 3 };
    std::cout << "[6,2,8,3] . [1,8,5,3] = " << dot(c, d, 4) << std::endl;

    glm::vec2 v(2, 1);
    std::cout << "same direction: " << glm::dot(v, glm::vec2(3, 1)) << std::endl;
    std::cout << "perpendicular:  " << glm::dot(v, glm::vec2(-1, 2)) << std::endl;
    std::cout << "opposite:       " << glm::dot(v, glm::vec2(-3, -1)) << std::endl;

    std::cin.get();
}
