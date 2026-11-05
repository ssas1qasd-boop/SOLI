#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <string>
#include <vector>
#include "stb_image.h"

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

    GLFWwindow* window = glfwCreateWindow(960, 480, "GPU copy", nullptr, nullptr);
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
        -0.9f, -0.9f,    0.0f, 0.0f,
         0.9f, -0.9f,    1.0f, 0.0f,
         0.9f,  0.9f,    1.0f, 1.0f,
        -0.9f,  0.9f,    0.0f, 1.0f
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
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void*)(2 * sizeof(float)));
    glEnableVertexAttribArray(1);

    GLuint tex[2];
    glGenTextures(2, tex);
    for (int flip = 0; flip < 2; flip++)
    {
        stbi_set_flip_vertically_on_load(flip);
        int width, height, channels;
        unsigned char* data = stbi_load("res/letter.png", &width, &height, &channels, 0);
        std::cout << "flip = " << flip << ": " << width << " x " << height << ", " << channels << " channels, first pixel in memory = ("
                  << (int)data[0] << ", " << (int)data[1] << ", " << (int)data[2] << ")" << std::endl;

        glBindTexture(GL_TEXTURE_2D, tex[flip]);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
        stbi_image_free(data);

        std::vector<unsigned char> back(width * height * 3);
        glPixelStorei(GL_PACK_ALIGNMENT, 1);
        glGetTexImage(GL_TEXTURE_2D, 0, GL_RGB, GL_UNSIGNED_BYTE, back.data());
        std::cout << "         CPU copy freed. read back from the GPU: " << back.size() << " bytes, first pixel = ("
                  << (int)back[0] << ", " << (int)back[1] << ", " << (int)back[2] << ")" << std::endl;
    }

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

        glViewport(0, 0, 960, 480);
        glClear(GL_COLOR_BUFFER_BIT);
        glBindVertexArray(vao);
        glActiveTexture(GL_TEXTURE0);
        for (int i = 0; i < 2; i++)
        {
            glViewport(i * 480 + 4, 4, 472, 472);
            glBindTexture(GL_TEXTURE_2D, tex[i]);
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteTextures(2, tex);
    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
