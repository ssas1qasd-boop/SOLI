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

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(960, 480, "Atlas", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    const int CELLS = 4;
    const int CELL = 16;
    const int SIZE = CELLS * CELL;
    std::vector<unsigned char> pixels(SIZE * SIZE * 3);
    for (int y = 0; y < SIZE; y++)
        for (int x = 0; x < SIZE; x++)
        {
            int cell = (y / CELL) * CELLS + x / CELL;
            bool mark = (x % CELL) < 4 && (y % CELL) < 4;
            pixels[(y * SIZE + x) * 3 + 0] = mark ? 255 : (cell % 4) * 70;
            pixels[(y * SIZE + x) * 3 + 1] = mark ? 255 : (cell / 4) * 70;
            pixels[(y * SIZE + x) * 3 + 2] = mark ? 255 : 160;
        }

    int pick[4] = { 0, 5, 10, 15 };
    GLfloat vertices[4 * 4 * 4 + 4 * 4];
    int k = 0;
    for (int q = 0; q < 5; q++)
    {
        float x0 = -0.98f + q * 0.395f, x1 = x0 + 0.37f;
        float u0 = 0.0f, v0 = 0.0f, u1 = 1.0f, v1 = 1.0f;
        if (q < 4)
        {
            int col = pick[q] % CELLS, row = pick[q] / CELLS;
            u0 = (float)col / CELLS;
            v0 = (float)row / CELLS;
            u1 = u0 + 1.0f / CELLS;
            v1 = v0 + 1.0f / CELLS;
            std::cout << "cell " << pick[q] << ": column " << col << ", row " << row << " -> u " << u0 << " .. " << u1 << ", v " << v0 << " .. " << v1 << std::endl;
        }
        GLfloat corner[16] = { x0, -0.37f, u0, v0,   x1, -0.37f, u1, v0,   x1, 0.37f, u1, v1,   x0, 0.37f, u0, v1 };
        for (int i = 0; i < 16; i++)
            vertices[k++] = corner[i];
    }
    GLuint indices[5 * 6];
    for (int q = 0; q < 5; q++)
    {
        GLuint b = q * 4;
        GLuint quad[6] = { b, b + 1, b + 2, b + 2, b + 3, b };
        for (int i = 0; i < 6; i++)
            indices[q * 6 + i] = quad[i];
    }
    std::cout << "5 quads: " << sizeof(vertices) << " bytes of vertices, " << sizeof(indices) << " bytes of indices, 1 texture, 1 draw call" << std::endl;

    GLuint vao, vbo, ebo;
    glGenVertexArrays(1, &vao);
    glBindVertexArray(vao);
    glGenBuffers(1, &vbo);
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glGenBuffers(1, &ebo);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void*)(2 * sizeof(float)));
    glEnableVertexAttribArray(1);

    GLuint tex;
    glGenTextures(1, &tex);
    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, tex);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, SIZE, SIZE, 0, GL_RGB, GL_UNSIGNED_BYTE, pixels.data());

    std::string vertexShader =
        "#version 330 core\n"
        "layout (location = 0) in vec2 aPos;\n"
        "layout (location = 1) in vec2 aTex;\n"
        "out vec2 texCoord;\n"
        "void main()\n"
        "{\n"
        "    gl_Position = vec4(aPos, 0.0, 1.0);\n"
        "    texCoord = aTex;\n"
        "}\n";

    std::string fragmentShader =
        "#version 330 core\n"
        "in vec2 texCoord;\n"
        "out vec4 FragColor;\n"
        "uniform sampler2D tex0;\n"
        "void main()\n"
        "{\n"
        "    FragColor = texture(tex0, texCoord);\n"
        "}\n";

    GLuint shaderProgram = CreateShader(vertexShader, fragmentShader);
    glUseProgram(shaderProgram);
    glUniform1i(glGetUniformLocation(shaderProgram, "tex0"), 0);
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);

    while (!glfwWindowShouldClose(window))
    {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);

        glClear(GL_COLOR_BUFFER_BIT);
        glBindVertexArray(vao);
        glDrawElements(GL_TRIANGLES, 5 * 6, GL_UNSIGNED_INT, 0);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteTextures(1, &tex);
    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
