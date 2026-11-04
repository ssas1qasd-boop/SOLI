#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <vector>

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

struct Polyline
{
    int first;
    int count;
};

std::vector<float> points;
std::vector<Polyline> polylines;
unsigned int buffer;

static void UploadPoints()
{
    glBindBuffer(GL_ARRAY_BUFFER, buffer);
    glBufferData(GL_ARRAY_BUFFER, points.size() * sizeof(float), points.data(), GL_DYNAMIC_DRAW);
}

static void MouseButtonCallback(GLFWwindow* window, int button, int action, int mods)
{
    if (action != GLFW_PRESS)
        return;

    if (button == GLFW_MOUSE_BUTTON_RIGHT)
    {
        std::cout << "right click: polyline " << polylines.size() - 1 << " finished" << std::endl;
        polylines.push_back({ (int)points.size() / 2, 0 });
        return;
    }

    double px, py;
    glfwGetCursorPos(window, &px, &py);
    int width, height;
    glfwGetWindowSize(window, &width, &height);
    points.push_back((float)(2.0 * px / width - 1.0));
    points.push_back((float)(1.0 - 2.0 * py / height));
    polylines.back().count++;
    std::cout << "left click: polyline " << polylines.size() - 1 << " has " << polylines.back().count << " points" << std::endl;

    UploadPoints();
}

static void KeyCallback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
    if (action != GLFW_PRESS || key != GLFW_KEY_BACKSPACE)
        return;

    if (polylines.back().count == 0)
    {
        if (polylines.size() == 1)
        {
            std::cout << "backspace: nothing to delete" << std::endl;
            return;
        }
        polylines.pop_back();
    }

    Polyline last = polylines.back();
    polylines.pop_back();
    for (int i = 0; i < last.count * 2; i++)
        points.pop_back();

    polylines.push_back({ (int)points.size() / 2, 0 });
    std::cout << "backspace: deleted a line of " << last.count << " points, "
              << polylines.size() - 1 << " lines left" << std::endl;
    UploadPoints();
}

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(640, 480, "Delete Last Line", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    unsigned int vao;
    glGenVertexArrays(1, &vao);
    glBindVertexArray(vao);

    glGenBuffers(1, &buffer);
    glBindBuffer(GL_ARRAY_BUFFER, buffer);

    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 2, 0);

    unsigned int shader = CreateShader(vertexShaderSrc, fragmentShaderSrc);
    glUseProgram(shader);
    int location = glGetUniformLocation(shader, "u_Color");
    glPointSize(10.0f);

    polylines.push_back({ 0, 0 });
    glfwSetMouseButtonCallback(window, MouseButtonCallback);
    glfwSetKeyCallback(window, KeyCallback);

    while (!glfwWindowShouldClose(window))
    {
        glClear(GL_COLOR_BUFFER_BIT);

        glUniform4f(location, 1.0f, 1.0f, 1.0f, 1.0f);
        for (const Polyline& line : polylines)
            glDrawArrays(GL_LINE_STRIP, line.first, line.count);

        glUniform4f(location, 1.0f, 0.5f, 0.1f, 1.0f);
        glDrawArrays(GL_POINTS, 0, (int)points.size() / 2);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shader);
    glfwTerminate();
    return 0;
}
