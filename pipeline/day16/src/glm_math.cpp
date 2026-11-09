#include <iostream>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#define GLM_ENABLE_EXPERIMENTAL
#include <glm/gtx/string_cast.hpp>

int main()
{
    glm::vec3 a(1.0f, 2.0f, 3.0f);
    glm::vec3 b(4.0f, 5.0f, 6.0f);
    std::cout << "a + b = " << glm::to_string(a + b) << std::endl;
    std::cout << "dot(a, b) = " << glm::dot(a, b) << ", cross(a, b) = " << glm::to_string(glm::cross(a, b)) << std::endl;
    std::cout << "length(a) = " << glm::length(a) << std::endl;

    glm::mat4 T = glm::translate(glm::mat4(1.0f), glm::vec3(7.0f, 3.0f, 5.0f));
    std::cout << "translate(7, 3, 5) * (1, -1, 2, 1) = " << glm::to_string(T * glm::vec4(1.0f, -1.0f, 2.0f, 1.0f)) << std::endl;

    const float* p = glm::value_ptr(T);
    std::cout << "value_ptr: p[12], p[13], p[14] = " << p[12] << ", " << p[13] << ", " << p[14] << "  (column-major: the 4th column is stored last)" << std::endl;
    std::cout << "T[3] (the 4th column) = " << glm::to_string(T[3]) << std::endl;

    glm::mat4 R = glm::rotate(glm::mat4(1.0f), glm::radians(90.0f), glm::vec3(0.0f, 0.0f, 1.0f));
    glm::vec4 nose(1.0f, 0.0f, 0.0f, 1.0f);
    glm::vec4 spin = T * R * nose;
    glm::vec4 orbit = R * T * nose;
    std::cout << "T * R * (1, 0, 0, 1) = (" << spin.x << ", " << spin.y << ", " << spin.z << ")" << std::endl;
    std::cout << "R * T * (1, 0, 0, 1) = (" << orbit.x << ", " << orbit.y << ", " << orbit.z << ")" << std::endl;

    glm::mat4 chained = glm::rotate(T, glm::radians(90.0f), glm::vec3(0.0f, 0.0f, 1.0f));
    std::cout << "glm::rotate(T, ...) == T * R ? " << (chained == T * R ? "yes" : "no") << std::endl;
    std::cout << "sizeof(glm::vec3) = " << sizeof(glm::vec3) << ", sizeof(glm::mat4) = " << sizeof(glm::mat4) << std::endl;
    return 0;
}
