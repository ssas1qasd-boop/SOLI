#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <string>
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

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(960, 480, "GLM", nullptr, nullptr);
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
        -0.5f, -0.25f,   1.0f, 0.5f, 0.2f,
         0.5f, -0.25f,   1.0f, 0.5f, 0.2f,
         0.5f,  0.25f,   0.2f, 0.6f, 1.0f,
        -0.5f,  0.25f,   0.2f, 0.6f, 1.0f
    };
    GLuint indices[] = {
        0, 1, 2,
        2, 3, 0
    };
    GLuint vao, vbo, ebo;
    glGenVertexArrays(1, &vao);
    glBindVertexArray(vao);
    glGenBuffers(1, &vbo);
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glGenBuffers(1, &ebo);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(2 * sizeof(float)));
    glEnableVertexAttribArray(1);

    glm::mat4 asInVideo = glm::mat4(1.0f);
    asInVideo = glm::rotate(asInVideo, 90.0f, glm::vec3(0.0f, 0.0f, 1.0f));
    asInVideo = glm::scale(asInVideo, glm::vec3(0.5f, 0.5f, 0.5f));

    glm::mat4 inRadians = glm::mat4(1.0f);
    inRadians = glm::rotate(inRadians, glm::radians(90.0f), glm::vec3(0.0f, 0.0f, 1.0f));
    inRadians = glm::scale(inRadians, glm::vec3(0.5f, 0.5f, 0.5f));

    glm::vec4 corner = glm::vec4(0.5f, -0.25f, 0.0f, 1.0f);
    glm::vec4 a = asInVideo * corner;
    glm::vec4 b = inRadians * corner;
    std::cout << "rotate(90.0f): corner (0.5, -0.25) -> (" << a.x << ", " << a.y << ")" << std::endl;
    std::cout << "rotate(radians(90)): corner (0.5, -0.25) -> (" << b.x << ", " << b.y << ")" << std::endl;
    std::cout << "90 radians = " << glm::degrees(90.0f) << " degrees = " << glm::degrees(90.0f) - 14 * 360 << " degrees after 14 full turns" << std::endl;

    std::string vertexShader =
        "#version 330 core\n"
        "layout (location = 0) in vec2 aPos;\n"
        "layout (location = 1) in vec3 aColor;\n"
        "out vec3 color;\n"
        "uniform mat4 transform;\n"
        "void main()\n"
        "{\n"
        "    gl_Position = transform * vec4(aPos, 0.0, 1.0);\n"
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
    GLint transformLoc = glGetUniformLocation(shaderProgram, "transform");
    glm::mat4 transforms[2] = { asInVideo, inRadians };
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);

    while (!glfwWindowShouldClose(window))
    {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);

        glViewport(0, 0, 960, 480);
        glClear(GL_COLOR_BUFFER_BIT);
        glBindVertexArray(vao);
        for (int i = 0; i < 2; i++)
        {
            glViewport(i * 480 + 4, 4, 472, 472);
            glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm::value_ptr(transforms[i]));
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
