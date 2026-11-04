#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>

static const char* vertexShaderSrc = R"(#version 330 core
layout(location = 0) in vec2 aPosition;
void main()
{
    gl_Position = vec4(aPosition, 0.0, 1.0);
})";

static const char* fragmentShaderSrc = R"(#version 330 core
uniform vec4 u_Color;
out vec4 color;
void main()
{
    color = u_Color;
})";

static unsigned int CompileShader(unsigned int type, const char* source)
{
    unsigned int id = glCreateShader(type);
    glShaderSource(id, 1, &source, nullptr);
    glCompileShader(id);
    int result;
    glGetShaderiv(id, GL_COMPILE_STATUS, &result);
    if (result == GL_FALSE)
    {
        char message[512];
        glGetShaderInfoLog(id, 512, nullptr, message);
        std::cout << "Shader error: " << message << std::endl;
    }
    return id;
}

static unsigned int CreateShader(const char* vertexSrc, const char* fragmentSrc)
{
    unsigned int program = glCreateProgram();
    unsigned int vs = CompileShader(GL_VERTEX_SHADER, vertexSrc);
    unsigned int fs = CompileShader(GL_FRAGMENT_SHADER, fragmentSrc);
    glAttachShader(program, vs);
    glAttachShader(program, fs);
    glLinkProgram(program);
    glDeleteShader(vs);
    glDeleteShader(fs);
    return program;
}

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(640, 480, "Two VAOs", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    float house[24] = {
        -0.4f, -0.5f,   0.4f, -0.5f,
         0.4f, -0.5f,   0.4f,  0.1f,
         0.4f,  0.1f,  -0.4f,  0.1f,
        -0.4f,  0.1f,  -0.4f, -0.5f,
        -0.5f,  0.1f,   0.0f,  0.6f,
         0.0f,  0.6f,   0.5f,  0.1f
    };

    float sun[8] = {
        0.6f, 0.7f,   0.8f, 0.7f,
        0.7f, 0.6f,   0.7f, 0.8f
    };

    unsigned int houseVao, houseBuffer;
    glGenVertexArrays(1, &houseVao);
    glBindVertexArray(houseVao);
    glGenBuffers(1, &houseBuffer);
    glBindBuffer(GL_ARRAY_BUFFER, houseBuffer);
    glBufferData(GL_ARRAY_BUFFER, 24 * sizeof(float), house, GL_STATIC_DRAW);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 2, 0);

    unsigned int sunVao, sunBuffer;
    glGenVertexArrays(1, &sunVao);
    glBindVertexArray(sunVao);
    glGenBuffers(1, &sunBuffer);
    glBindBuffer(GL_ARRAY_BUFFER, sunBuffer);
    glBufferData(GL_ARRAY_BUFFER, 8 * sizeof(float), sun, GL_STATIC_DRAW);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 2, 0);

    glBindVertexArray(0);
    glBindBuffer(GL_ARRAY_BUFFER, 0);

    unsigned int shader = CreateShader(vertexShaderSrc, fragmentShaderSrc);
    glUseProgram(shader);
    int location = glGetUniformLocation(shader, "u_Color");

    while (!glfwWindowShouldClose(window))
    {
        glClear(GL_COLOR_BUFFER_BIT);

        glBindVertexArray(houseVao);
        glUniform4f(location, 1.0f, 1.0f, 1.0f, 1.0f);
        glDrawArrays(GL_LINES, 0, 12);

        glBindVertexArray(sunVao);
        glUniform4f(location, 1.0f, 0.8f, 0.1f, 1.0f);
        glDrawArrays(GL_LINES, 0, 4);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shader);
    glfwTerminate();
    return 0;
}
