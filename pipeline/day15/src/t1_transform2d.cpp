#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <string>
#include <cmath>

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

struct Mat3
{
    float m[3][3];
};

Mat3 Multiply(const Mat3& a, const Mat3& b)
{
    Mat3 r = {};
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            for (int k = 0; k < 3; k++)
                r.m[i][j] += a.m[i][k] * b.m[k][j];
    return r;
}

Mat3 Translate(float tx, float ty)
{
    return { { { 1, 0, tx }, { 0, 1, ty }, { 0, 0, 1 } } };
}

Mat3 Rotate(float degrees)
{
    float t = degrees * 3.14159265f / 180.0f;
    return { { { std::cos(t), -std::sin(t), 0 }, { std::sin(t), std::cos(t), 0 }, { 0, 0, 1 } } };
}

Mat3 Scale(float sx, float sy)
{
    return { { { sx, 0, 0 }, { 0, sy, 0 }, { 0, 0, 1 } } };
}

void PrintMat(const char* name, const Mat3& a)
{
    std::cout << name << ":";
    for (int i = 0; i < 3; i++)
        std::cout << "  [" << a.m[i][0] << ", " << a.m[i][1] << ", " << a.m[i][2] << "]";
    std::cout << std::endl;
}

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(640, 640, "Transform 2D", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    GLfloat house[] = {
        0.3f, 0.2f,   0.6f, 0.2f,   0.6f, 0.5f,
        0.6f, 0.5f,   0.3f, 0.5f,   0.3f, 0.2f,
        0.3f, 0.5f,   0.6f, 0.5f,   0.45f, 0.7f
    };
    GLuint vao, vbo;
    glGenVertexArrays(1, &vao);
    glBindVertexArray(vao);
    glGenBuffers(1, &vbo);
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(house), house, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    Mat3 aroundOrigin = Rotate(90);
    Mat3 aroundCenter = Multiply(Translate(0.45f, 0.4f), Multiply(Rotate(90), Translate(-0.45f, -0.4f)));
    Mat3 moved = Multiply(Translate(-0.9f, -0.9f), Scale(1.5f, 0.5f));
    PrintMat("rotate 90 around (0, 0)", aroundOrigin);
    PrintMat("T(c) R T(-c), c = (0.45, 0.4)", aroundCenter);
    PrintMat("T(-0.9, -0.9) S(1.5, 0.5)", moved);
    float x = 0.6f, y = 0.2f;
    std::cout << "corner (0.6, 0.2): around origin -> (" << aroundOrigin.m[0][0] * x + aroundOrigin.m[0][1] * y + aroundOrigin.m[0][2]
              << ", " << aroundOrigin.m[1][0] * x + aroundOrigin.m[1][1] * y + aroundOrigin.m[1][2] << "), around center -> ("
              << aroundCenter.m[0][0] * x + aroundCenter.m[0][1] * y + aroundCenter.m[0][2] << ", " << aroundCenter.m[1][0] * x + aroundCenter.m[1][1] * y + aroundCenter.m[1][2] << ")" << std::endl;

    std::string vertexShader =
        "#version 330 core\n"
        "layout (location = 0) in vec2 aPos;\n"
        "uniform mat3 u_M;\n"
        "void main()\n"
        "{\n"
        "    vec3 p = u_M * vec3(aPos, 1.0);\n"
        "    gl_Position = vec4(p.xy, 0.0, 1.0);\n"
        "}\n";

    std::string fragmentShader =
        "#version 330 core\n"
        "out vec4 FragColor;\n"
        "uniform vec4 u_Color;\n"
        "void main()\n"
        "{\n"
        "    FragColor = u_Color;\n"
        "}\n";

    GLuint shaderProgram = CreateShader(vertexShader, fragmentShader);
    glUseProgram(shaderProgram);
    GLint matLoc = glGetUniformLocation(shaderProgram, "u_M");
    GLint colorLoc = glGetUniformLocation(shaderProgram, "u_Color");
    Mat3 identity = Scale(1, 1);
    Mat3 shapes[4] = { identity, aroundOrigin, aroundCenter, moved };
    float colors[4][3] = { { 0.6f, 0.6f, 0.6f }, { 0.15f, 0.39f, 0.92f }, { 0.92f, 0.35f, 0.05f }, { 0.09f, 0.64f, 0.29f } };
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);

    while (!glfwWindowShouldClose(window))
    {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);

        glClear(GL_COLOR_BUFFER_BIT);
        glBindVertexArray(vao);
        for (int i = 0; i < 4; i++)
        {
            glUniformMatrix3fv(matLoc, 1, GL_TRUE, &shapes[i].m[0][0]);
            glUniform4f(colorLoc, colors[i][0], colors[i][1], colors[i][2], 1.0f);
            glDrawArrays(GL_TRIANGLES, 0, 9);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
