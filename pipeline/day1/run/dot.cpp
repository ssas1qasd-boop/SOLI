// Dot product examples from 3Blue1Brown chapter 9, computed in C++ (and with GLM).
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
    float a[] = {1, 2},        b[] = {3, 4};
    float c[] = {6, 2, 8, 3},  d[] = {1, 8, 5, 3};
    std::cout << "[1,2] . [3,4]         = " << dot(a, b, 2) << "\n";
    std::cout << "[6,2,8,3] . [1,8,5,3] = " << dot(c, d, 4) << "\n\n";

    std::cout << "1x2 matrix [1 -2] times [4,3] = " << glm::dot(glm::vec2(1, -2), glm::vec2(4, 3)) << "\n\n";

    glm::vec2 v(2, 1);
    std::cout << "sign test with v = (2,1):\n";
    std::cout << "  v . (3, 1)   = " << glm::dot(v, glm::vec2(3, 1))   << "   positive -> same direction\n";
    std::cout << "  v . (-1, 2)  = " << glm::dot(v, glm::vec2(-1, 2))  << "   zero     -> perpendicular\n";
    std::cout << "  v . (-3, -1) = " << glm::dot(v, glm::vec2(-3, -1)) << "   negative -> opposite\n\n";

    glm::vec2 u = glm::normalize(glm::vec2(1, 1));
    glm::vec2 x(3, 1);
    std::cout << "unit u = (" << u.x << ", " << u.y << ")\n";
    std::cout << "u . (3,1)       = " << glm::dot(u, x) << "   (shadow length of x on u)\n";
    std::cout << "(3u) . (3,1)    = " << glm::dot(3.0f * u, x) << "   (3x bigger)\n";
    std::cout << "order: v.x = " << glm::dot(v, x) << ", x.v = " << glm::dot(x, v) << "\n";
}
