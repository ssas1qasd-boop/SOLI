#include <iostream>
#include <cmath>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

float R(float v) { return std::round(v * 1000) / 1000 + 0.0f; }

int main()
{
    float alpha = glm::radians(30.0f), beta = glm::radians(45.0f);
    float x1 = std::cos(alpha), y1 = std::sin(alpha);
    float x2 = x1 * std::cos(beta) - y1 * std::sin(beta);
    float y2 = x1 * std::sin(beta) + y1 * std::cos(beta);
    std::cout << "start (" << R(x1) << ", " << R(y1) << ") at 30 degrees, turn 45" << std::endl;
    std::cout << "formula:      (" << R(x2) << ", " << R(y2) << ")" << std::endl;
    std::cout << "cos/sin(75):  (" << R(std::cos(alpha + beta)) << ", " << R(std::sin(alpha + beta)) << ")" << std::endl;

    float angle = 0.0f;
    for (int frame = 0; frame < 60; frame++)
        angle += 6.0f;
    std::cout << "60 frames x 6 degrees = " << angle << " degrees (one full turn per second at 60 fps)" << std::endl;

    float b = glm::radians(90.0f);
    float rx[3][3] = { { 1, 0, 0 }, { 0, std::cos(b), -std::sin(b) }, { 0, std::sin(b), std::cos(b) } };
    float ry[3][3] = { { std::cos(b), 0, std::sin(b) }, { 0, 1, 0 }, { -std::sin(b), 0, std::cos(b) } };
    glm::mat4 gx = glm::rotate(glm::mat4(1.0f), b, glm::vec3(1, 0, 0));
    glm::mat4 gy = glm::rotate(glm::mat4(1.0f), b, glm::vec3(0, 1, 0));
    float worst = 0;
    for (int row = 0; row < 3; row++)
        for (int col = 0; col < 3; col++)
        {
            worst = std::fmax(worst, std::fabs(rx[row][col] - gx[col][row]));
            worst = std::fmax(worst, std::fabs(ry[row][col] - gy[col][row]));
        }
    std::cout << "hand Rx, Ry (row by row) vs glm::rotate: biggest difference " << worst << std::endl;
    std::cout << "Rx row 1 = (" << R(rx[1][0]) << ", " << R(rx[1][1]) << ", " << R(rx[1][2]) << "), Ry row 2 = (" << R(ry[2][0]) << ", " << R(ry[2][1]) << ", " << R(ry[2][2]) << ")" << std::endl;
    return 0;
}
