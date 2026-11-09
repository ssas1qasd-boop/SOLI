#include <iostream>
#include <cmath>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

int main()
{
    const float WindowWidth = 800.0f, WindowHeight = 600.0f;
    const float AspectRatio = WindowWidth / WindowHeight;
    const float FieldOfView = glm::radians(45.0f);
    glm::mat4 Projection = glm::perspective(FieldOfView, AspectRatio, 0.1f, 100.0f);
    glm::mat4 View = glm::lookAt(glm::vec3(0, 0, 5), glm::vec3(0, 0, 0), glm::vec3(0, 1, 0));

    float MouseX = 600.0f, MouseY = 150.0f;
    float WindowX = MouseX;
    float WindowY = WindowHeight - MouseY;
    std::cout << "1. GLFW mouse (" << MouseX << ", " << MouseY << ") -> window from the bottom (" << WindowX << ", " << WindowY << ")" << std::endl;

    float CenterX = WindowWidth / 2, CenterY = WindowHeight / 2;
    float NdcX = (WindowX - CenterX) / (WindowWidth / 2);
    float NdcY = (WindowY - CenterY) / (WindowHeight / 2);
    std::cout << "2. NDC (" << NdcX << ", " << NdcY << ")" << std::endl;

    float FocalLength = 1.0f / std::tan(FieldOfView / 2);
    glm::vec3 ViewSpaceVector(NdcX * AspectRatio / FocalLength, NdcY / FocalLength, -1.0f);
    std::cout << "3. focal length " << FocalLength << ", view space ray (" << ViewSpaceVector.x << ", " << ViewSpaceVector.y << ", " << ViewSpaceVector.z << ")" << std::endl;

    glm::vec4 Anton = glm::inverse(Projection) * glm::vec4(NdcX, NdcY, -1.0f, 1.0f);
    Anton = glm::vec4(Anton.x / -Anton.z, Anton.y / -Anton.z, -1.0f, 0.0f);
    std::cout << "   Anton (inverse projection): (" << Anton.x << ", " << Anton.y << ", " << Anton.z << ")" << std::endl;

    glm::vec3 ObjectWorld(0.0f, 0.0f, 0.0f);
    float ObjectViewZ = (View * glm::vec4(ObjectWorld, 1.0f)).z;
    glm::vec3 IntersectionPoint = ViewSpaceVector * -ObjectViewZ;
    std::cout << "4. object view z " << ObjectViewZ << ", intersection in view space (" << IntersectionPoint.x << ", " << IntersectionPoint.y << ", " << IntersectionPoint.z << ")" << std::endl;

    glm::vec4 NewWorldPosition = glm::inverse(View) * glm::vec4(IntersectionPoint, 1.0f);
    std::cout << "5. new world position (" << NewWorldPosition.x << ", " << NewWorldPosition.y << ", " << NewWorldPosition.z << ")" << std::endl;

    glm::vec4 clip = Projection * View * NewWorldPosition;
    glm::vec3 ndc = glm::vec3(clip) / clip.w;
    float backX = CenterX + WindowWidth / 2 * ndc.x;
    float backY = WindowHeight - (CenterY + WindowHeight / 2 * ndc.y);
    std::cout << "check: the object projects back to mouse (" << std::round(backX * 100) / 100 << ", " << std::round(backY * 100) / 100 << ")" << std::endl;
    return 0;
}
