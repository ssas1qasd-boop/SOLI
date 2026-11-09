#include <iostream>
#include <cmath>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

void Where(const char* name, const glm::mat4& M)
{
    glm::vec4 p = M * glm::vec4(0.0f, 0.0f, 0.0f, 1.0f);
    std::cout << name << " at (" << std::round(p.x * 100) / 100 + 0.0f << ", " << std::round(p.y * 100) / 100 + 0.0f << ")" << std::endl;
}

int main()
{
    glm::mat4 chairs[4];
    for (int i = 0; i < 4; i++)
    {
        chairs[i] = glm::rotate(glm::mat4(1.0f), glm::radians(90.0f * i), glm::vec3(0, 0, 1));
        chairs[i] = glm::translate(chairs[i], glm::vec3(1.5f, 0.0f, 0.0f));
    }

    glm::mat4 table = glm::mat4(1.0f);
    std::cout << "table at the origin:" << std::endl;
    for (int i = 0; i < 4; i++)
        Where("  chair", table * chairs[i]);

    table = glm::translate(glm::mat4(1.0f), glm::vec3(10.0f, 5.0f, 0.0f));
    table = glm::rotate(table, glm::radians(45.0f), glm::vec3(0, 0, 1));
    std::cout << "table moved to (10, 5) and turned 45:" << std::endl;
    Where("  table", table);
    for (int i = 0; i < 4; i++)
        Where("  chair", table * chairs[i]);
    return 0;
}
