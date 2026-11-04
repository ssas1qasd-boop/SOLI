#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <string>

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

    GLFWwindow* window = glfwCreateWindow(640, 480, "Two Methods", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    float square[8] = {
        -0.35f, -0.35f,
         0.05f, -0.35f,
         0.05f,  0.05f,
        -0.35f,  0.05f
    };

    unsigned int squareIndices[6] = {
        0, 1, 2,
        2, 3, 0
    };

    float triangle[9] = {
        -0.30f, 0.15f, 0.0f,
         0.30f, 0.15f, 0.0f,
         0.00f, 0.55f, 0.0f
    };

    unsigned int squareBuffer, squareIbo, triangleBuffer;
    glGenBuffers(1, &squareBuffer);
    glGenBuffers(1, &squareIbo);
    glGenBuffers(1, &triangleBuffer);

    // ---------- method 2: one VAO per object (the layout is stored once)
    unsigned int squareVao;
    glGenVertexArrays(1, &squareVao);
    glBindVertexArray(squareVao);
    glBindBuffer(GL_ARRAY_BUFFER, squareBuffer);
    glBufferData(GL_ARRAY_BUFFER, 8 * sizeof(float), square, GL_STATIC_DRAW);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 2, 0);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, squareIbo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 6 * sizeof(unsigned int), squareIndices, GL_STATIC_DRAW);

    unsigned int triangleVao;
    glGenVertexArrays(1, &triangleVao);
    glBindVertexArray(triangleVao);
    glBindBuffer(GL_ARRAY_BUFFER, triangleBuffer);
    glBufferData(GL_ARRAY_BUFFER, 9 * sizeof(float), triangle, GL_STATIC_DRAW);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, 0);

    // ---------- method 1: one global VAO, the layout is set again before every draw
    unsigned int globalVao;
    glGenVertexArrays(1, &globalVao);
    glBindVertexArray(globalVao);
    glEnableVertexAttribArray(0);
    glBindVertexArray(0);

    std::string vertexShader =
        "#version 330 core\n"
        "\n"
        "layout(location = 0) in vec4 position;\n"
        "uniform vec2 u_Offset;\n"
        "\n"
        "void main()\n"
        "{\n"
        "    gl_Position = vec4(position.xy + u_Offset, 0.0, 1.0);\n"
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
    int offsetLocation = glGetUniformLocation(shader, "u_Offset");

    int frame = 0;

    while (!glfwWindowShouldClose(window))
    {
        glClear(GL_COLOR_BUFFER_BIT);

        // left half: method 2, one bind per object
        glUniform2f(offsetLocation, -0.45f, 0.0f);
        glBindVertexArray(squareVao);
        glUniform4f(colorLocation, 1.0f, 0.5f, 0.1f, 1.0f);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);
        glBindVertexArray(triangleVao);
        glUniform4f(colorLocation, 0.2f, 0.6f, 1.0f, 1.0f);
        glDrawArrays(GL_TRIANGLES, 0, 3);

        // right half: method 1, buffer + layout again before each draw
        glUniform2f(offsetLocation, 0.45f, 0.0f);
        glBindVertexArray(globalVao);
        glBindBuffer(GL_ARRAY_BUFFER, squareBuffer);
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 2, 0);
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, squareIbo);
        glUniform4f(colorLocation, 1.0f, 0.5f, 0.1f, 1.0f);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);
        glBindBuffer(GL_ARRAY_BUFFER, triangleBuffer);
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, 0);
        glUniform4f(colorLocation, 0.2f, 0.6f, 1.0f, 1.0f);
        glDrawArrays(GL_TRIANGLES, 0, 3);

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
