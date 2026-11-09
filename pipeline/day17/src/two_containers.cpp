#include <iostream>
#include <cmath>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

void Corner(const char* name, const glm::mat4& M)
{
    glm::vec4 c = M * glm::vec4(0.5f, 0.5f, 0.0f, 1.0f);
    std::cout << name << " corner (0.5, 0.5) -> (" << std::round(c.x * 100) / 100 + 0.0f << ", " << std::round(c.y * 100) / 100 + 0.0f << ")" << std::endl;
}

int main()
{
    for (int second = 0; second <= 2; second++)
    {
        float time = second * 0.7854f;
        std::cout << "time = " << time << " s" << std::endl;

        glm::mat4 first = glm::mat4(1.0f);
        first = glm::translate(first, glm::vec3(0.5f, -0.5f, 0.0f));
        first = glm::rotate(first, time, glm::vec3(0.0f, 0.0f, 1.0f));
        Corner("  container 1 (translate, rotate)", first);

        glm::mat4 swapped = glm::mat4(1.0f);
        swapped = glm::rotate(swapped, time, glm::vec3(0.0f, 0.0f, 1.0f));
        swapped = glm::translate(swapped, glm::vec3(0.5f, -0.5f, 0.0f));
        Corner("  swapped (rotate, translate) ", swapped);

        float s = std::sin(time);
        glm::mat4 second2 = glm::mat4(1.0f);
        second2 = glm::translate(second2, glm::vec3(-0.5f, 0.5f, 0.0f));
        second2 = glm::scale(second2, glm::vec3(s, s, s));
        Corner("  container 2 (scale by sin)   ", second2);
    }
    return 0;
}
