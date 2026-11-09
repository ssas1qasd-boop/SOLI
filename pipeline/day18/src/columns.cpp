#include <iostream>
#include <cmath>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

void Print(const char* name, glm::vec3 v)
{
    std::cout << name << " (" << std::round(v.x * 1000) / 1000 + 0.0f << ", " << std::round(v.y * 1000) / 1000 + 0.0f << ", " << std::round(v.z * 1000) / 1000 + 0.0f << ")" << std::endl;
}

int main()
{
    glm::mat3 M(glm::vec3(0, 0, -1), glm::vec3(0, 1, 0), glm::vec3(1, 0, 0));
    glm::vec3 v(1, 2, 3);

    Print("M * (1, 2, 3)               =", M * v);
    Print("1*M[0] + 2*M[1] + 3*M[2]    =", v.x * M[0] + v.y * M[1] + v.z * M[2]);

    glm::mat3 fromGlm(glm::rotate(glm::mat4(1.0f), glm::radians(90.0f), glm::vec3(0, 1, 0)));
    Print("glm::rotate(90, y) column 0 =", fromGlm[0]);
    Print("glm::rotate(90, y) column 2 =", fromGlm[2]);

    glm::mat3 shear(glm::vec3(1, 0, 0), glm::vec3(1, 1, 0), glm::vec3(0, 0, 1));
    Print("shear * (M * v)             =", shear * (M * v));
    Print("(shear * M) * v             =", (shear * M) * v);
    Print("(M * shear) * v             =", (M * shear) * v);
    Print("column 0 of shear * M       =", (shear * M)[0]);
    Print("shear * (where i goes, M[0])=", shear * M[0]);
    return 0;
}
