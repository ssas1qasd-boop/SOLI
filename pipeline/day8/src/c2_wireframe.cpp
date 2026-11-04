#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <string>
#include <vector>

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

class Vertex
{
public:
    float x, y, z;
};

class Edge
{
public:
    int v0, v1;
};

class Face
{
public:
    std::vector<int> edges;
};

int main()
{
    std::vector<Vertex> vertices = { {0, 0, 0}, {1, 0, 0}, {1, 1, 0}, {0, 1, 0},
                                     {0, 0, 1}, {1, 0, 1}, {1, 1, 1}, {0, 1, 1} };
    std::vector<Edge> edges = { {0, 1}, {1, 2}, {2, 3}, {3, 0},
                                {4, 5}, {5, 6}, {6, 7}, {7, 4},
                                {0, 4}, {1, 5}, {2, 6}, {3, 7} };
    std::vector<Face> faces = { {{0, 1, 2, 3}}, {{4, 5, 6, 7}}, {{0, 9, 4, 8}},
                                {{1, 10, 5, 9}}, {{2, 11, 6, 10}}, {{3, 8, 7, 11}} };
    std::cout << "V = " << vertices.size() << ", E = " << edges.size() << ", F = " << faces.size()
              << ", F - E + V = " << (int)faces.size() - (int)edges.size() + (int)vertices.size() << std::endl;

    std::vector<float> screen;
    for (const Vertex& v : vertices)
    {
        screen.push_back((v.x - 0.5f) * 0.9f + (v.y - 0.5f) * 0.45f);
        screen.push_back((v.z - 0.5f) * 0.9f + (v.y - 0.5f) * 0.35f);
    }

    std::vector<unsigned int> lines;
    for (const Edge& e : edges)
    {
        lines.push_back(e.v0);
        lines.push_back(e.v1);
    }

    std::vector<unsigned int> frontLines;
    for (int e : faces[2].edges)
    {
        frontLines.push_back(edges[e].v0);
        frontLines.push_back(edges[e].v1);
    }
    std::cout << "lines to draw: " << lines.size() / 2 << ", front face lines: " << frontLines.size() / 2 << std::endl;

    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(640, 480, "B-Rep Wireframe", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    unsigned int buffer;
    glGenBuffers(1, &buffer);
    glBindBuffer(GL_ARRAY_BUFFER, buffer);
    glBufferData(GL_ARRAY_BUFFER, screen.size() * sizeof(float), screen.data(), GL_STATIC_DRAW);

    unsigned int allVao;
    glGenVertexArrays(1, &allVao);
    glBindVertexArray(allVao);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 2, 0);
    unsigned int allIbo;
    glGenBuffers(1, &allIbo);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, allIbo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, lines.size() * sizeof(unsigned int), lines.data(), GL_STATIC_DRAW);

    unsigned int frontVao;
    glGenVertexArrays(1, &frontVao);
    glBindVertexArray(frontVao);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 2, 0);
    unsigned int frontIbo;
    glGenBuffers(1, &frontIbo);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, frontIbo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, frontLines.size() * sizeof(unsigned int), frontLines.data(), GL_STATIC_DRAW);

    std::string vertexShader =
        "#version 330 core\n"
        "\n"
        "layout(location = 0) in vec4 position;\n"
        "\n"
        "void main()\n"
        "{\n"
        "    gl_Position = position;\n"
        "}\n";

    std::string fragmentShader =
        "#version 330 core\n"
        "\n"
        "layout(location = 0) out vec4 color;\n"
        "\n"
        "uniform vec4 u_Color;\n"
        "\n"
        "void main()\n"
        "{\n"
        "    color = u_Color;\n"
        "}\n";

    unsigned int shader = CreateShader(vertexShader, fragmentShader);
    glUseProgram(shader);
    int colorLocation = glGetUniformLocation(shader, "u_Color");
    glPointSize(10.0f);
    glLineWidth(3.0f);

    int frame = 0;
    while (!glfwWindowShouldClose(window))
    {
        glClear(GL_COLOR_BUFFER_BIT);

        glBindVertexArray(allVao);
        glUniform4f(colorLocation, 0.85f, 0.85f, 0.85f, 1.0f);
        glDrawElements(GL_LINES, (int)lines.size(), GL_UNSIGNED_INT, nullptr);
        glUniform4f(colorLocation, 0.3f, 0.7f, 1.0f, 1.0f);
        glDrawArrays(GL_POINTS, 0, (int)vertices.size());

        glBindVertexArray(frontVao);
        glUniform4f(colorLocation, 1.0f, 0.5f, 0.1f, 1.0f);
        glDrawElements(GL_LINES, (int)frontLines.size(), GL_UNSIGNED_INT, nullptr);

        if (frame == 0)
            std::cout << "frame 0 drawn, glGetError() = " << glGetError() << std::endl;
        frame++;

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shader);
    glfwTerminate();
    return 0;
}
