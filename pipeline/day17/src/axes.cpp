#include <iostream>
#include <cmath>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

void Show(const char* name, glm::vec4 p)
{
    std::cout << name << " (" << std::round(p.x * 1000) / 1000 + 0.0f << ", " << std::round(p.y * 1000) / 1000 + 0.0f << ", " << std::round(p.z * 1000) / 1000 + 0.0f << ")" << std::endl;
}

int main()
{
    glm::mat4 I(1.0f);
    glm::vec4 p(1.0f, 0.0f, 0.0f, 1.0f);
    glm::vec4 q(0.0f, 1.0f, 0.0f, 1.0f);
    Show("Rz(90) * (1, 0, 0) =", glm::rotate(I, glm::radians(90.0f), glm::vec3(0, 0, 1)) * p);
    Show("Rx(90) * (0, 1, 0) =", glm::rotate(I, glm::radians(90.0f), glm::vec3(1, 0, 0)) * q);
    Show("Ry(90) * (1, 0, 0) =", glm::rotate(I, glm::radians(90.0f), glm::vec3(0, 1, 0)) * p);

    glm::mat4 Rx = glm::rotate(I, glm::radians(90.0f), glm::vec3(1, 0, 0));
    glm::mat4 Ry = glm::rotate(I, glm::radians(90.0f), glm::vec3(0, 1, 0));
    Show("Rx * Ry * (1, 0, 0) =", Rx * Ry * p);
    Show("Ry * Rx * (1, 0, 0) =", Ry * Rx * p);

    glm::vec3 axis = glm::normalize(glm::vec3(1.0f, 1.0f, 1.0f));
    glm::mat4 R = glm::rotate(I, glm::radians(120.0f), axis);
    Show("R(120, (1,1,1)) * (1, 0, 0) =", R * p);
    Show("R(120, (1,1,1)) * (0, 1, 0) =", R * q);

    glm::mat3 R3(R);
    glm::mat3 check = R3 * glm::transpose(R3);
    std::cout << "R * R^T diagonal = " << check[0][0] << ", " << check[1][1] << ", " << check[2][2] << ",  det(R) = " << glm::determinant(R3) << std::endl;
    std::cout << "length before = " << glm::length(glm::vec3(p)) << ", after = " << glm::length(glm::vec3(R * p)) << std::endl;
    return 0;
}
