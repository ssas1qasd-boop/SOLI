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

struct Matrix4f
{
    float m[4][4];
};

Matrix4f RotationZ(float angleInRadians)
{
    float c = std::cos(angleInRadians), s = std::sin(angleInRadians);
    return { { { c, -s, 0, 0 },
               { s, c, 0, 0 },
               { 0, 0, 1, 0 },
               { 0, 0, 0, 1 } } };
}

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(960, 320, "Rotation Z", nullptr, nullptr);
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
        -0.6f, -0.4f, 0.0f,   0.86f, 0.15f, 0.15f,
        0.6f, -0.4f, 0.0f,   0.09f, 0.64f, 0.29f,
        0.0f, 0.7f, 0.0f,   0.15f, 0.39f, 0.92f
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

    float AngleInRadians = 0.0f;
    float Delta = 0.0785f;
    Matrix4f snapshots[3];
    int keep = 0;
    for (int frame = 0; frame <= 40; frame++)
    {
        if (frame % 20 == 0)
        {
            snapshots[keep++] = RotationZ(AngleInRadians);
            std::cout << "frame " << frame << ": angle " << AngleInRadians << " rad, row 0 = (" << snapshots[keep - 1].m[0][0] << ", " << snapshots[keep - 1].m[0][1] + 0.0f << ")" << std::endl;
        }
        AngleInRadians += Delta;
        if (AngleInRadians >= 1.5708f || AngleInRadians <= -1.5708f)
            Delta *= -1.0f;
    }

    std::string vertexShader =
        "#version 330 core\n"
        "layout (location = 0) in vec3 aPos;\n"
        "layout (location = 1) in vec3 aColor;\n"
        "out vec3 color;\n"
        "uniform mat4 gRotation;\n"
        "void main()\n"
        "{\n"
        "    gl_Position = gRotation * vec4(aPos, 1.0);\n"
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
    GLint rotationLoc = glGetUniformLocation(shaderProgram, "gRotation");
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);

    while (!glfwWindowShouldClose(window))
    {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);

        glViewport(0, 0, 960, 320);
        glClear(GL_COLOR_BUFFER_BIT);
        glBindVertexArray(vao);
        for (int i = 0; i < 3; i++)
        {
            glViewport(i * 320, 0, 320, 320);
            glUniformMatrix4fv(rotationLoc, 1, GL_TRUE, &snapshots[i].m[0][0]);
            glDrawArrays(GL_TRIANGLES, 0, 3);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
