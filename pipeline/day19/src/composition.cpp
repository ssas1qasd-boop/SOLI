#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <string>
#include <vector>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

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

void AddBar(std::vector<float>& out, glm::vec2 a, glm::vec2 b, float half, glm::vec3 color)
{
    glm::vec2 d = glm::normalize(b - a);
    glm::vec2 n(-d.y * half, d.x * half);
    glm::vec2 quad[6] = { a - n, b - n, b + n, b + n, a + n, a - n };
    for (glm::vec2 p : quad)
        out.insert(out.end(), { p.x, p.y, color.r, color.g, color.b });
}

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(1000, 250, "Composition", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    std::vector<float> vertices;
    for (int k = -3; k <= 3; k++)
    {
        AddBar(vertices, glm::vec2(k, -3), glm::vec2(k, 3), 0.015f, glm::vec3(0.25f, 0.32f, 0.40f));
        AddBar(vertices, glm::vec2(-3, k), glm::vec2(3, k), 0.015f, glm::vec3(0.25f, 0.32f, 0.40f));
    }
    AddBar(vertices, glm::vec2(0, 0), glm::vec2(1, 0), 0.06f, glm::vec3(0.13f, 0.77f, 0.37f));
    AddBar(vertices, glm::vec2(0, 0), glm::vec2(0, 1), 0.06f, glm::vec3(0.94f, 0.27f, 0.27f));
    int count = (int)vertices.size() / 5;

    GLuint vao, vbo;
    glGenVertexArrays(1, &vao);
    glBindVertexArray(vao);
    glGenBuffers(1, &vbo);
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(float), vertices.data(), GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(2 * sizeof(float)));
    glEnableVertexAttribArray(1);

    glm::mat2 rotation(glm::vec2(0, 1), glm::vec2(-1, 0));
    glm::mat2 shear(glm::vec2(1, 0), glm::vec2(1, 1));
    glm::mat2 steps[4] = { glm::mat2(1.0f), rotation, shear * rotation, rotation * shear };
    const char* names[4] = { "identity", "rotation", "shear * rotation", "rotation * shear" };
    for (int i = 0; i < 4; i++)
        std::cout << names[i] << ": i -> (" << steps[i][0].x << ", " << steps[i][0].y << "), j -> (" << steps[i][1].x << ", " << steps[i][1].y << ")" << std::endl;

    std::string vertexShader =
        "#version 330 core\n"
        "layout (location = 0) in vec2 aPos;\n"
        "layout (location = 1) in vec3 aColor;\n"
        "out vec3 color;\n"
        "uniform mat2 linear;\n"
        "void main()\n"
        "{\n"
        "    gl_Position = vec4(0.3 * (linear * aPos), 0.0, 1.0);\n"
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
    GLint linearLoc = glGetUniformLocation(shaderProgram, "linear");
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);

    while (!glfwWindowShouldClose(window))
    {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);

        glViewport(0, 0, 1000, 250);
        glClear(GL_COLOR_BUFFER_BIT);
        glBindVertexArray(vao);
        for (int i = 0; i < 4; i++)
        {
            glViewport(i * 250, 0, 250, 250);
            glUniformMatrix2fv(linearLoc, 1, GL_FALSE, glm::value_ptr(steps[i]));
            glDrawArrays(GL_TRIANGLES, 0, count);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
