#include <iostream>
#include <glm/glm.hpp>

void Show(const char* name, const glm::mat2& m)
{
    std::cout << name << " = [ " << m[0][0] << " " << m[1][0] << " ; " << m[0][1] << " " << m[1][1] << " ]  (columns (" << m[0].x << ", " << m[0].y << ") and (" << m[1].x << ", " << m[1].y << "))" << std::endl;
}

int main()
{
    glm::mat2 M1(glm::vec2(1, 1), glm::vec2(-2, 0));
    glm::mat2 M2(glm::vec2(0, 1), glm::vec2(2, 0));
    Show("M1     ", M1);
    Show("M2     ", M2);

    glm::vec2 firstColumn = M2 * M1[0];
    glm::vec2 secondColumn = M2 * M1[1];
    std::cout << "M2 * (1, 1) = (" << firstColumn.x << ", " << firstColumn.y << "),  M2 * (-2, 0) = (" << secondColumn.x << ", " << secondColumn.y << ")" << std::endl;
    Show("M2 * M1", M2 * M1);
    Show("M1 * M2", M1 * M2);

    glm::mat2 A(glm::vec2(2, 0), glm::vec2(0, 1));
    glm::mat2 B(glm::vec2(0, 1), glm::vec2(-1, 0));
    glm::mat2 C(glm::vec2(1, 0), glm::vec2(1, 1));
    glm::vec2 v(3, -1);
    glm::vec2 left = ((A * B) * C) * v;
    glm::vec2 right = (A * (B * C)) * v;
    glm::vec2 oneByOne = A * (B * (C * v));
    std::cout << "(A B) C v = (" << left.x << ", " << left.y << "),  A (B C) v = (" << right.x << ", " << right.y << "),  A(B(C v)) = (" << oneByOne.x << ", " << oneByOne.y << ")" << std::endl;
    return 0;
}
