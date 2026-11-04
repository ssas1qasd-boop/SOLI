#define GLM_ENABLE_EXPERIMENTAL
#include <cstdio>
#include <glm/glm.hpp>
#include <glm/gtx/rotate_vector.hpp>
// same math as Camera.cpp: speed 0.1, sensitivity 100, window 800x800
int main() {
    glm::vec3 Up(0, 1, 0);
    glm::vec3 P(0, 0, 2), O(0, 0, -1);
    for (int i = 0; i < 10; i++) P += 0.1f * O;                       // W x 10
    printf("W10: P=(%.2f, %.2f, %.2f)\n", P.x, P.y, P.z);
    P = glm::vec3(0, 0, 2);
    for (int i = 0; i < 10; i++) P += 0.1f * glm::normalize(glm::cross(O, Up));   // D x 10
    printf("D10: P=(%.2f, %.2f, %.2f)\n", P.x, P.y, P.z);
    // mouse 100 px right of centre for 2 frames (cursor is re-centred every frame)
    for (int i = 0; i < 2; i++) {
        float rotY = 100.0f * (float)(500 - 400) / 800;
        O = glm::rotate(O, glm::radians(-rotY), Up);
        printf("mouse frame %d: rotY=%.1f deg  O=(%.2f, %.2f, %.2f)\n", i + 1, rotY, O.x, O.y, O.z);
    }
}
