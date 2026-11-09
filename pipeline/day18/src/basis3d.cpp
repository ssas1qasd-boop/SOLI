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

    GLFWwindow* window = glfwCreateWindow(960, 400, "Basis 3D", nullptr, nullptr);
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

    glm::vec3 iHat(1, 0, 0), jHat(0, 1, 0), kHat(0, 0, 1);
    glm::mat3 identity(iHat, jHat, kHat);
    glm::mat3 rotateY(glm::vec3(0, 0, -1), glm::vec3(0, 1, 0), glm::vec3(1, 0, 0));
    glm::mat3 shear(glm::vec3(1, 0, 0), glm::vec3(1, 1, 0), glm::vec3(0, 0, 1));
    glm::mat3 linear[3] = { identity, rotateY, shear };
    const char* names[3] = { "identity", "rotate 90 around y", "shear (j -> (1, 1, 0))" };

    glm::mat4 tilt = glm::rotate(glm::mat4(1.0f), glm::radians(20.0f), glm::vec3(1, 0, 0));
    tilt = glm::rotate(tilt, glm::radians(-30.0f), glm::vec3(0, 1, 0));
    glm::mat4 models[3];
    for (int i = 0; i < 3; i++)
    {
        models[i] = glm::scale(tilt * glm::mat4(linear[i]), glm::vec3(0.4f));
        glm::vec3 p = linear[i] * glm::vec3(1, 2, 3);
        std::cout << names[i] << ": columns i=(" << linear[i][0].x << ", " << linear[i][0].y << ", " << linear[i][0].z << ")"
                  << " k=(" << linear[i][2].x << ", " << linear[i][2].y << ", " << linear[i][2].z << ")"
                  << ", (1, 2, 3) -> (" << p.x << ", " << p.y << ", " << p.z << ")" << std::endl;
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

        glViewport(0, 0, 960, 400);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glBindVertexArray(vao);
        for (int i = 0; i < 3; i++)
        {
            glViewport(i * 320 + 20, 60, 280, 280);
            glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(models[i]));
            glDrawArrays(GL_TRIANGLES, 0, 36);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
