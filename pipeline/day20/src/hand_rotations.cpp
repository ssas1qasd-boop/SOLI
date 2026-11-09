#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <string>
#include <cmath>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

static unsigned int CompileShader(unsigned int type, const std::string& source)
{
    unsigned int id = glCreateShader(type);
    const char* src = source.c_str();
    glShaderSource(id, 1, &src, nullptr);
    glCompileShader(id);

    int result;
    glGetShaderiv(id, GL_COMPILE_STATUS, &result);
    if (result == GL_FALSE)
    {
        int length;
        glGetShaderiv(id, GL_INFO_LOG_LENGTH, &length);
        char* message = new char[length];
        glGetShaderInfoLog(id, length, &length, message);
        std::cout << "Failed to compile "
                  << (type == GL_VERTEX_SHADER ? "vertex" : "fragment")
                  << " shader!" << std::endl;
        std::cout << message << std::endl;
        delete[] message;
        glDeleteShader(id);
        return 0;
    }

    return id;
}

static unsigned int CreateShader(const std::string& vertexShader, const std::string& fragmentShader)
{
    unsigned int program = glCreateProgram();
    unsigned int vs = CompileShader(GL_VERTEX_SHADER, vertexShader);
    unsigned int fs = CompileShader(GL_FRAGMENT_SHADER, fragmentShader);

    glAttachShader(program, vs);
    glAttachShader(program, fs);
    glLinkProgram(program);
    glValidateProgram(program);

    glDeleteShader(vs);
    glDeleteShader(fs);

    return program;
}

struct Matrix4f
{
    float m[4][4];
};

Matrix4f Identity()
{
    return { { { 1, 0, 0, 0 }, { 0, 1, 0, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 1 } } };
}

Matrix4f RotationX(float a)
{
    Matrix4f r = Identity();
    r.m[1][1] = std::cos(a); r.m[1][2] = -std::sin(a);
    r.m[2][1] = std::sin(a); r.m[2][2] = std::cos(a);
    return r;
}

Matrix4f RotationY(float a)
{
    Matrix4f r = Identity();
    r.m[0][0] = std::cos(a); r.m[0][2] = std::sin(a);
    r.m[2][0] = -std::sin(a); r.m[2][2] = std::cos(a);
    return r;
}

Matrix4f RotationZ(float a)
{
    Matrix4f r = Identity();
    r.m[0][0] = std::cos(a); r.m[0][1] = -std::sin(a);
    r.m[1][0] = std::sin(a); r.m[1][1] = std::cos(a);
    return r;
}

Matrix4f Scale(float s)
{
    Matrix4f r = Identity();
    r.m[0][0] = s; r.m[1][1] = s; r.m[2][2] = s;
    return r;
}

Matrix4f operator*(const Matrix4f& a, const Matrix4f& b)
{
    Matrix4f r;
    for (int row = 0; row < 4; row++)
        for (int col = 0; col < 4; col++)
        {
            r.m[row][col] = 0;
            for (int k = 0; k < 4; k++)
                r.m[row][col] += a.m[row][k] * b.m[k][col];
        }
    return r;
}

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(960, 360, "Hand Rotations", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    GLfloat vertices[] = {
        // front (+z) red
        -1.0f, -1.0f, 1.0f,   0.86f, 0.15f, 0.15f,
        1.0f, -1.0f, 1.0f,   0.86f, 0.15f, 0.15f,
        1.0f, 1.0f, 1.0f,   0.86f, 0.15f, 0.15f,
        1.0f, 1.0f, 1.0f,   0.86f, 0.15f, 0.15f,
        -1.0f, 1.0f, 1.0f,   0.86f, 0.15f, 0.15f,
        -1.0f, -1.0f, 1.0f,   0.86f, 0.15f, 0.15f,
        // back (-z) orange
        -1.0f, -1.0f, -1.0f,   0.92f, 0.35f, 0.05f,
        -1.0f, 1.0f, -1.0f,   0.92f, 0.35f, 0.05f,
        1.0f, 1.0f, -1.0f,   0.92f, 0.35f, 0.05f,
        1.0f, 1.0f, -1.0f,   0.92f, 0.35f, 0.05f,
        1.0f, -1.0f, -1.0f,   0.92f, 0.35f, 0.05f,
        -1.0f, -1.0f, -1.0f,   0.92f, 0.35f, 0.05f,
        // top (+y) green
        -1.0f, 1.0f, -1.0f,   0.09f, 0.64f, 0.29f,
        -1.0f, 1.0f, 1.0f,   0.09f, 0.64f, 0.29f,
        1.0f, 1.0f, 1.0f,   0.09f, 0.64f, 0.29f,
        1.0f, 1.0f, 1.0f,   0.09f, 0.64f, 0.29f,
        1.0f, 1.0f, -1.0f,   0.09f, 0.64f, 0.29f,
        -1.0f, 1.0f, -1.0f,   0.09f, 0.64f, 0.29f,
        // bottom (-y) blue
        -1.0f, -1.0f, -1.0f,   0.15f, 0.39f, 0.92f,
        1.0f, -1.0f, -1.0f,   0.15f, 0.39f, 0.92f,
        1.0f, -1.0f, 1.0f,   0.15f, 0.39f, 0.92f,
        1.0f, -1.0f, 1.0f,   0.15f, 0.39f, 0.92f,
        -1.0f, -1.0f, 1.0f,   0.15f, 0.39f, 0.92f,
        -1.0f, -1.0f, -1.0f,   0.15f, 0.39f, 0.92f,
        // right (+x) purple
        1.0f, -1.0f, -1.0f,   0.49f, 0.23f, 0.93f,
        1.0f, 1.0f, -1.0f,   0.49f, 0.23f, 0.93f,
        1.0f, 1.0f, 1.0f,   0.49f, 0.23f, 0.93f,
        1.0f, 1.0f, 1.0f,   0.49f, 0.23f, 0.93f,
        1.0f, -1.0f, 1.0f,   0.49f, 0.23f, 0.93f,
        1.0f, -1.0f, -1.0f,   0.49f, 0.23f, 0.93f,
        // left (-x) yellow
        -1.0f, -1.0f, -1.0f,   0.92f, 0.70f, 0.03f,
        -1.0f, -1.0f, 1.0f,   0.92f, 0.70f, 0.03f,
        -1.0f, 1.0f, 1.0f,   0.92f, 0.70f, 0.03f,
        -1.0f, 1.0f, 1.0f,   0.92f, 0.70f, 0.03f,
        -1.0f, 1.0f, -1.0f,   0.92f, 0.70f, 0.03f,
        -1.0f, -1.0f, -1.0f,   0.92f, 0.70f, 0.03f
    };
    GLuint vao, vbo;
    glGenVertexArrays(1, &vao);
    glBindVertexArray(vao);
    glGenBuffers(1, &vbo);
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    float angle = glm::radians(40.0f);
    Matrix4f rotations[3] = { RotationX(angle), RotationY(angle), RotationZ(angle) };
    glm::vec3 axes[3] = { glm::vec3(1, 0, 0), glm::vec3(0, 1, 0), glm::vec3(0, 0, 1) };
    const char* names[3] = { "RotationX", "RotationY", "RotationZ" };
    Matrix4f models[3];
    for (int i = 0; i < 3; i++)
    {
        models[i] = rotations[i] * Scale(0.45f);
        glm::mat4 g = glm::rotate(glm::mat4(1.0f), angle, axes[i]);
        float worst = 0;
        for (int row = 0; row < 4; row++)
            for (int col = 0; col < 4; col++)
                worst = std::fmax(worst, std::fabs(rotations[i].m[row][col] - g[col][row]));
        std::cout << names[i] << "(40): hand-made vs glm::rotate, biggest difference " << worst << std::endl;
    }

    std::string vertexShader =
        "#version 330 core\n"
        "layout (location = 0) in vec3 aPos;\n"
        "layout (location = 1) in vec3 aColor;\n"
        "out vec3 color;\n"
        "uniform mat4 model;\n"
        "void main()\n"
        "{\n"
        "    gl_Position = model * vec4(aPos, 1.0);\n"
        "    gl_Position.z = -gl_Position.z;\n"
        "    color = aColor;\n"
        "}\n";

    std::string fragmentShader =
        "#version 330 core\n"
        "in vec3 color;\n"
        "out vec4 FragColor;\n"
        "void main()\n"
        "{\n"
        "    FragColor = vec4(color, 1.0);\n"
        "}\n";

    GLuint shaderProgram = CreateShader(vertexShader, fragmentShader);
    glUseProgram(shaderProgram);
    GLint modelLoc = glGetUniformLocation(shaderProgram, "model");
    glEnable(GL_DEPTH_TEST);
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);

    while (!glfwWindowShouldClose(window))
    {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);

        glViewport(0, 0, 960, 360);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glBindVertexArray(vao);
        for (int i = 0; i < 3; i++)
        {
            glViewport(i * 320 + 20, 40, 280, 280);
            glUniformMatrix4fv(modelLoc, 1, GL_TRUE, &models[i].m[0][0]);
            glDrawArrays(GL_TRIANGLES, 0, 36);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
