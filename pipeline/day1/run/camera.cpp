// Camera class from "OpenGL Tutorial 8 - Camera" (Victor Gordan).
// Xvfb has no real keyboard/mouse, so Inputs() reads a small "Keys" struct.
// The real program fills it from GLFW; here we fill it by hand to SIMULATE key presses.
// Every movement / rotation line is the same as in the video.
#include "common.h"
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#define GLM_ENABLE_EXPERIMENTAL
#include <glm/gtx/rotate_vector.hpp>
#include <glm/gtx/vector_angle.hpp>

struct Keys { bool W=0,A=0,S=0,D=0,Space=0,Ctrl=0,Shift=0,MouseLeft=0; double mouseX=0, mouseY=0; };

class Camera
{
public:
    glm::vec3 Position;
    glm::vec3 Orientation = glm::vec3(0.0f, 0.0f, -1.0f);
    glm::vec3 Up = glm::vec3(0.0f, 1.0f, 0.0f);
    int width, height;
    float speed = 0.1f;
    float sensitivity = 100.0f;
    bool firstClick = true;

    Camera(int width, int height, glm::vec3 position)
    {
        Camera::width = width;
        Camera::height = height;
        Position = position;
    }

    void Matrix(float FOVdeg, float nearPlane, float farPlane, unsigned int shaderID, const char* uniform)
    {
        glm::mat4 view = glm::lookAt(Position, Position + Orientation, Up);
        glm::mat4 projection = glm::perspective(glm::radians(FOVdeg), (float)width / height, nearPlane, farPlane);
        glUniformMatrix4fv(glGetUniformLocation(shaderID, uniform), 1, GL_FALSE, glm::value_ptr(projection * view));
    }

    void Inputs(Keys& k)
    {
        if (k.W) Position += speed * Orientation;
        if (k.A) Position += speed * -glm::normalize(glm::cross(Orientation, Up));
        if (k.S) Position += speed * -Orientation;
        if (k.D) Position += speed * glm::normalize(glm::cross(Orientation, Up));
        if (k.Space) Position += speed * Up;
        if (k.Ctrl)  Position += speed * -Up;
        if (k.Shift) speed = 0.4f; else speed = 0.1f;

        if (k.MouseLeft)
        {
            if (firstClick) { /* glfwSetCursorPos(center) */ firstClick = false; }
            double mouseX = k.mouseX, mouseY = k.mouseY;      // glfwGetCursorPos(window, &mouseX, &mouseY)
            float rotX = sensitivity * (float)(mouseY - (height / 2)) / height;
            float rotY = sensitivity * (float)(mouseX - (width / 2)) / width;

            glm::vec3 newOrientation = glm::rotate(Orientation, glm::radians(-rotX), glm::normalize(glm::cross(Orientation, Up)));
            if (!(glm::angle(newOrientation, Up) <= glm::radians(5.0f) || glm::angle(newOrientation, -Up) <= glm::radians(5.0f)))
                Orientation = newOrientation;
            Orientation = glm::rotate(Orientation, glm::radians(-rotY), Up);
            /* glfwSetCursorPos(window, width/2, height/2) */
        }
        else firstClick = true;
    }
};

static const char* vs = R"(#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
out vec3 color;
uniform mat4 camMatrix;
void main() { gl_Position = camMatrix * vec4(aPos, 1.0); color = aColor; })";

static const char* fs = R"(#version 330 core
in vec3 color;
out vec4 FragColor;
void main() { FragColor = vec4(color, 1.0); })";

const int W = 800, H = 800;
unsigned int shader, vaoP, vaoG; int gridCount;

void Draw(Camera& cam, float fov, const char* file)
{
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glUseProgram(shader);
    cam.Matrix(fov, 0.1f, 100.0f, shader, "camMatrix");
    glBindVertexArray(vaoG); glDrawArrays(GL_LINES, 0, gridCount);
    glBindVertexArray(vaoP); glDrawElements(GL_TRIANGLES, 18, GL_UNSIGNED_INT, 0);
    SaveScreenshot(file, W, H);
    printf("%-22s Position=(%.2f, %.2f, %.2f)  Orientation=(%.2f, %.2f, %.2f)\n", file,
        cam.Position.x, cam.Position.y, cam.Position.z, cam.Orientation.x, cam.Orientation.y, cam.Orientation.z);
}

unsigned int MakeVAO(const std::vector<float>& v, const std::vector<unsigned>* idx)
{
    unsigned int vao, vbo, ebo;
    glGenVertexArrays(1, &vao); glBindVertexArray(vao);
    glGenBuffers(1, &vbo); glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, v.size() * 4, v.data(), GL_STATIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, (void*)0);  glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, (void*)12); glEnableVertexAttribArray(1);
    if (idx) { glGenBuffers(1, &ebo); glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
               glBufferData(GL_ELEMENT_ARRAY_BUFFER, idx->size() * 4, idx->data(), GL_STATIC_DRAW); }
    return vao;
}

int main()
{
    GLFWwindow* window = MakeWindow(W, H, "Camera");
    glEnable(GL_DEPTH_TEST);
    shader = CreateShader(vs, fs);

    // pyramid (same shape as the tutorial; vertex colors instead of the brick texture)
    // each face gets its own color; scene sits at y = -0.5 so the camera sees it from slightly above
    const float B = -0.5f, T = 0.3f;
    glm::vec3 p0(-0.5f,B, 0.5f), p1(-0.5f,B,-0.5f), p2(0.5f,B,-0.5f), p3(0.5f,B,0.5f), top(0,T,0);
    glm::vec3 cBase(0.55f,0.45f,0.35f), cFront(0.95f,0.62f,0.25f), cRight(0.30f,0.62f,0.95f),
              cBack(0.45f,0.82f,0.45f), cLeft(0.88f,0.38f,0.55f);
    std::vector<float> pyr; std::vector<unsigned> ind;
    auto tri = [&](glm::vec3 a, glm::vec3 b, glm::vec3 c, glm::vec3 col) {
        for (glm::vec3 p : {a, b, c}) { pyr.insert(pyr.end(), {p.x,p.y,p.z, col.r,col.g,col.b}); ind.push_back(ind.size()); } };
    tri(p0,p1,p2,cBase); tri(p0,p2,p3,cBase);
    tri(p3,p0,top,cFront); tri(p2,p3,top,cRight); tri(p1,p2,top,cBack); tri(p0,p1,top,cLeft);
    vaoP = MakeVAO(pyr, &ind);

    std::vector<float> grid;   // floor grid so movement is visible
    for (int i = -5; i <= 5; i++) {
        float g = (i == 0) ? 0.45f : 0.25f;
        float a[] = { (float)i,-0.501f,-5, g,g,g, (float)i,-0.501f,5, g,g,g,
                      -5,-0.501f,(float)i, g,g,g,  5,-0.501f,(float)i, g,g,g };
        grid.insert(grid.end(), a, a + 24);
    }
    gridCount = grid.size() / 6;
    vaoG = MakeVAO(grid, nullptr);

    auto fresh = [] { return Camera(W, H, glm::vec3(0.0f, 0.0f, 2.0f)); };
    auto hold = [](Camera& c, Keys k, int frames) { for (int i = 0; i < frames; i++) c.Inputs(k); };

    { Camera c = fresh(); Draw(c, 45, "out/cam_start.ppm"); }
    { Camera c = fresh(); Keys k; k.W = 1; hold(c, k, 10); Draw(c, 45, "out/cam_W.ppm"); }
    { Camera c = fresh(); Keys k; k.S = 1; hold(c, k, 10); Draw(c, 45, "out/cam_S.ppm"); }
    { Camera c = fresh(); Keys k; k.D = 1; hold(c, k, 10); Draw(c, 45, "out/cam_D.ppm"); }
    { Camera c = fresh(); Keys k; k.Space = 1; hold(c, k, 8); Draw(c, 45, "out/cam_Space.ppm"); }
    { Camera c = fresh(); Keys k; k.W = 1; k.D = 1; hold(c, k, 8); Draw(c, 45, "out/cam_WD.ppm"); }
    { Camera c = fresh(); Keys k; k.MouseLeft = 1; k.mouseX = W/2 + 100; k.mouseY = H/2; hold(c, k, 2); Draw(c, 45, "out/cam_mouseR.ppm"); }
    { Camera c = fresh(); Keys k; k.Space = 1; hold(c, k, 10);
      Keys m; m.MouseLeft = 1; m.mouseX = W/2; m.mouseY = H/2 + 80; hold(c, m, 3); Draw(c, 45, "out/cam_mouseDown.ppm"); }
    { Camera c = fresh(); Draw(c, 90, "out/cam_fov90.ppm"); }

    printf("\n-- normal drag: mouse 40px up every frame (5 deg/frame) --\n");
    { Camera c = fresh(); Keys m; m.MouseLeft = 1; m.mouseX = W/2; m.mouseY = H/2 - 40;
      for (int f = 1; f <= 20; f++) { c.Inputs(m);
        if (f % 2 == 0 || f >= 16) printf("frame %2d: angle(Orientation, Up) = %5.1f deg   y = %.3f\n", f, glm::degrees(glm::angle(c.Orientation, c.Up)), c.Orientation.y); } }

    printf("\n-- very fast drag: mouse 300px up every frame (37.5 deg/frame) --\n");
    { Camera c = fresh(); Keys m; m.MouseLeft = 1; m.mouseX = W/2; m.mouseY = H/2 - 300;
      for (int f = 1; f <= 4; f++) { c.Inputs(m);
        printf("frame %d: angle(Orientation, Up) = %5.1f deg   Orientation.z = %+.2f %s\n", f, glm::degrees(glm::angle(c.Orientation, c.Up)),
               c.Orientation.z, c.Orientation.z > 0 ? "<- flipped: now looking BACKWARD" : ""); } }

    glfwTerminate();
}
