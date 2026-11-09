#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <string>
#include <cmath>
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

glm::vec3 DragTheObject(double mouseX, double mouseY, const glm::mat4& view, float objectViewZ)
{
    float ndcX = ((float)mouseX - 400.0f) / 400.0f;
    float ndcY = ((600.0f - (float)mouseY) - 300.0f) / 300.0f;
    float focalLength = 1.0f / std::tan(glm::radians(45.0f) / 2);
    glm::vec3 ray(ndcX * (800.0f / 600.0f) / focalLength, ndcY / focalLength, -1.0f);
    glm::vec3 hit = ray * -objectViewZ;
    return glm::vec3(glm::inverse(view) * glm::vec4(hit, 1.0f));
}

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(800, 600, "Drag", nullptr, nullptr);
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

    GLfloat cross[] = {
        -0.04f, -0.004f, 0.0f,   1, 1, 1,   0.04f, -0.004f, 0.0f,   1, 1, 1,   0.04f, 0.004f, 0.0f,   1, 1, 1,
        0.04f, 0.004f, 0.0f,   1, 1, 1,   -0.04f, 0.004f, 0.0f,   1, 1, 1,   -0.04f, -0.004f, 0.0f,   1, 1, 1,
        -0.003f, -0.053f, 0.0f,   1, 1, 1,   0.003f, -0.053f, 0.0f,   1, 1, 1,   0.003f, 0.053f, 0.0f,   1, 1, 1,
        0.003f, 0.053f, 0.0f,   1, 1, 1,   -0.003f, 0.053f, 0.0f,   1, 1, 1,   -0.003f, -0.053f, 0.0f,   1, 1, 1
    };
    GLuint crossVao, crossVbo;
    glGenVertexArrays(1, &crossVao);
    glBindVertexArray(crossVao);
    glGenBuffers(1, &crossVbo);
    glBindBuffer(GL_ARRAY_BUFFER, crossVbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(cross), cross, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    glm::mat4 projection = glm::perspective(glm::radians(45.0f), 800.0f / 600.0f, 0.1f, 100.0f);
    glm::mat4 view = glm::lookAt(glm::vec3(0, 0, 5), glm::vec3(0, 0, 0), glm::vec3(0, 1, 0));
    glm::vec3 positions[3] = { glm::vec3(-2, 0, 0), glm::vec3(0, 0, 0), glm::vec3(2, 0, 0) };
    int picked = 1;
    float objectViewZ = (view * glm::vec4(positions[picked], 1.0f)).z;
    double mouseX = 600.0, mouseY = 150.0;
    positions[picked] = DragTheObject(mouseX, mouseY, view, objectViewZ);
    std::cout << "cube " << picked << " dragged to (" << positions[picked].x << ", " << positions[picked].y << ", " << positions[picked].z << ")" << std::endl;

    std::string vertexShader =
        "#version 330 core\n"
        "layout (location = 0) in vec3 aPos;\n"
        "layout (location = 1) in vec3 aColor;\n"
        "out vec3 color;\n"
        "uniform mat4 mvp;\n"
        "void main()\n"
        "{\n"
        "    gl_Position = mvp * vec4(aPos, 1.0);\n"
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
    GLint mvpLoc = glGetUniformLocation(shaderProgram, "mvp");
    glEnable(GL_DEPTH_TEST);
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);

    while (!glfwWindowShouldClose(window))
    {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);
        if (glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_PRESS)
        {
            glfwGetCursorPos(window, &mouseX, &mouseY);
            positions[picked] = DragTheObject(mouseX, mouseY, view, objectViewZ);
        }

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glBindVertexArray(vao);
        for (int i = 0; i < 3; i++)
        {
            glm::mat4 model = glm::translate(glm::mat4(1.0f), positions[i]);
            model = glm::rotate(model, glm::radians(30.0f), glm::vec3(1, 1, 0));
            model = glm::scale(model, glm::vec3(0.4f));
            glm::mat4 mvp = projection * view * model;
            glUniformMatrix4fv(mvpLoc, 1, GL_FALSE, glm::value_ptr(mvp));
            glDrawArrays(GL_TRIANGLES, 0, 36);
        }

        glm::mat4 atMouse = glm::translate(glm::mat4(1.0f), glm::vec3(((float)mouseX - 400.0f) / 400.0f, (300.0f - (float)mouseY) / 300.0f, -0.99f));
        glUniformMatrix4fv(mvpLoc, 1, GL_FALSE, glm::value_ptr(atMouse));
        glBindVertexArray(crossVao);
        glDrawArrays(GL_TRIANGLES, 0, 12);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
