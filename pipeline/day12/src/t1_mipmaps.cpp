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

    GLFWwindow* window = glfwCreateWindow(960, 640, "Mipmaps", nullptr, nullptr);
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
        -1.0f, -1.0f, 0.0f, 1.0f,    0.0f,  0.0f,
         1.0f, -1.0f, 0.0f, 1.0f,    2.0f,  0.0f,
         1.0f,  6.0f, 0.0f, 6.0f,    2.0f, 12.0f,
        -1.0f,  6.0f, 0.0f, 6.0f,    0.0f, 12.0f
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
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(4 * sizeof(float)));
    glEnableVertexAttribArray(1);

    const int SIZE = 256;
    std::vector<unsigned char> pixels(SIZE * SIZE * 3);
    for (int y = 0; y < SIZE; y++)
        for (int x = 0; x < SIZE; x++)
        {
            unsigned char c = ((x / 16 + y / 16) % 2 == 0) ? 240 : 20;
            pixels[(y * SIZE + x) * 3 + 0] = c;
            pixels[(y * SIZE + x) * 3 + 1] = c;
            pixels[(y * SIZE + x) * 3 + 2] = c;
        }

    GLuint tex;
    glGenTextures(1, &tex);
    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, tex);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, SIZE, SIZE, 0, GL_RGB, GL_UNSIGNED_BYTE, pixels.data());
    glGenerateMipmap(GL_TEXTURE_2D);

    GLint maxLevel = 0;
    for (int level = 0; level < 16; level++)
    {
        GLint w = 0;
        glGetTexLevelParameteriv(GL_TEXTURE_2D, level, GL_TEXTURE_WIDTH, &w);
        if (w == 0)
            break;
        std::cout << "mip level " << level << ": " << w << " x " << w << std::endl;
        maxLevel = level;
    }
    GLfloat maxAniso = 0.0f;
    glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY, &maxAniso);
    std::cout << "levels: " << maxLevel + 1 << ", GL_MAX_TEXTURE_MAX_ANISOTROPY = " << maxAniso << std::endl;

    std::string vertexShader =
        "#version 330 core\n"
        "layout (location = 0) in vec4 aPos;\n"
        "layout (location = 1) in vec2 aTex;\n"
        "out vec2 texCoord;\n"
        "void main()\n"
        "{\n"
        "    gl_Position = aPos;\n"
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
    GLint minFilters[] = { GL_NEAREST, GL_LINEAR, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR_MIPMAP_LINEAR };
    GLfloat aniso[] = { 1.0f, 1.0f, 1.0f, maxAniso };
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);

    while (!glfwWindowShouldClose(window))
    {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);

        glViewport(0, 0, 960, 640);
        glClear(GL_COLOR_BUFFER_BIT);
        glBindVertexArray(vao);
        for (int i = 0; i < 4; i++)
        {
            glViewport((i % 2) * 480 + 4, (1 - i / 2) * 320 + 4, 472, 312);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilters[i]);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY, aniso[i]);
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteTextures(1, &tex);
    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
