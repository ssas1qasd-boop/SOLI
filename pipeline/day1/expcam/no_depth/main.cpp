#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include "shaderClass.h"
#include "Camera.h"

const unsigned int width = 800;
const unsigned int height = 800;

const char* vertexSrc = R"(#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
out vec3 color;
uniform mat4 camMatrix;
void main()
{
    gl_Position = camMatrix * vec4(aPos, 1.0);
    color = aColor;
})";

const char* fragmentSrc = R"(#version 330 core
in vec3 color;
out vec4 FragColor;
void main()
{
    FragColor = vec4(color, 1.0);
})";

GLfloat vertices[] =
{
    -0.5f, -0.5f,  0.5f,   0.55f, 0.45f, 0.35f,
    -0.5f, -0.5f, -0.5f,   0.55f, 0.45f, 0.35f,
     0.5f, -0.5f, -0.5f,   0.55f, 0.45f, 0.35f,
     0.5f, -0.5f,  0.5f,   0.55f, 0.45f, 0.35f,
     0.5f, -0.5f,  0.5f,   0.95f, 0.62f, 0.25f,
    -0.5f, -0.5f,  0.5f,   0.95f, 0.62f, 0.25f,
     0.0f,  0.3f,  0.0f,   0.95f, 0.62f, 0.25f,
     0.5f, -0.5f, -0.5f,   0.30f, 0.62f, 0.95f,
     0.5f, -0.5f,  0.5f,   0.30f, 0.62f, 0.95f,
     0.0f,  0.3f,  0.0f,   0.30f, 0.62f, 0.95f,
    -0.5f, -0.5f, -0.5f,   0.45f, 0.82f, 0.45f,
     0.5f, -0.5f, -0.5f,   0.45f, 0.82f, 0.45f,
     0.0f,  0.3f,  0.0f,   0.45f, 0.82f, 0.45f,
    -0.5f, -0.5f,  0.5f,   0.88f, 0.38f, 0.55f,
    -0.5f, -0.5f, -0.5f,   0.88f, 0.38f, 0.55f,
     0.0f,  0.3f,  0.0f,   0.88f, 0.38f, 0.55f
};

GLuint indices[] =
{
    0, 1, 2,
    0, 2, 3,
    4, 5, 6,
    7, 8, 9,
    10, 11, 12,
    13, 14, 15
};

int main()
{
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(width, height, "Camera", nullptr, nullptr);
    if (window == nullptr)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    gladLoadGL();
    glViewport(0, 0, width, height);

    Shader shaderProgram(vertexSrc, fragmentSrc);

    GLuint VAO, VBO, EBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);


    Camera camera(width, height, glm::vec3(0.0f, 0.0f, 2.0f));

    while (!glfwWindowShouldClose(window))
    {
        glClearColor(0.07f, 0.13f, 0.17f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        shaderProgram.Activate();

        camera.Inputs(window);
        camera.Matrix(45.0f, 0.1f, 100.0f, shaderProgram, "camMatrix");

        glBindVertexArray(VAO);
        glDrawElements(GL_TRIANGLES, sizeof(indices) / sizeof(int), GL_UNSIGNED_INT, 0);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteBuffers(1, &EBO);
    shaderProgram.Delete();
    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}
