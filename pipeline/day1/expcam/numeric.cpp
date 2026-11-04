#include <iostream>
#include <cmath>
#define GLM_ENABLE_EXPERIMENTAL
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtx/rotate_vector.hpp>

int main()
{
    glm::vec3 Up(0, 1, 0);
    // 1) normalize: looking 60 degrees down
    glm::vec3 lookDown = glm::rotate(glm::vec3(0, 0, -1), glm::radians(-60.0f), glm::vec3(1, 0, 0));
    std::cout << "[normalize] looking 60 deg down:\n";
    std::cout << "  length of cross(Orientation, Up)            = " << glm::length(glm::cross(lookDown, Up)) << "\n";
    std::cout << "  length of normalize(cross(Orientation, Up)) = " << glm::length(glm::normalize(glm::cross(lookDown, Up))) << "\n\n";

    // 2) firstClick: first click with the mouse at (700, 100) in an 800x800 window
    float sensitivity = 100.0f; int width = 800, height = 800;
    float rotX = sensitivity * (float)(100 - (height / 2)) / height;
    float rotY = sensitivity * (float)(700 - (width / 2)) / width;
    std::cout << "[firstClick] mouse at (700,100) on the first click, without centering first:\n";
    std::cout << "  jump up/down    = " << rotX << " deg\n";
    std::cout << "  jump left/right = " << rotY << " deg   (in ONE frame)\n\n";

    // 3) the 5 degree check: what if Orientation becomes exactly Up?
    glm::vec3 pos(0, 0, 2);
    glm::mat4 v = glm::lookAt(pos, pos + Up, Up);
    std::cout << "[5 deg check] lookAt when looking straight up:\n";
    std::cout << "  view[0][0] = " << v[0][0] << "   (nan = not a number -> nothing can be drawn)\n";
    std::cout << "  cross(Up, Up) = (" << glm::cross(Up, Up).x << ", " << glm::cross(Up, Up).y << ", " << glm::cross(Up, Up).z << ")  -> no 'right' direction\n\n";

    // 4) (float)width / height
    int w = 800, h = 600;
    std::cout << "[float cast] window 800 x 600:\n";
    std::cout << "  width / height        = " << w / h << "     (int division: fraction lost)\n";
    std::cout << "  (float)width / height = " << (float)w / h << "\n";
}
