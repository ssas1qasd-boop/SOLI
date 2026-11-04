#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <string>
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

class Texture
{
public:
    GLuint ID;
    int width, height, channels;

    Texture(const char* path)
    {
        stbi_set_flip_vertically_on_load(true);
        unsigned char* bytes = stbi_load(path, &width, &height, &channels, 0);
        GLenum format = (channels == 4) ? GL_RGBA : GL_RGB;

        glGenTextures(1, &ID);
        glBindTexture(GL_TEXTURE_2D, ID);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexImage2D(GL_TEXTURE_2D, 0, format, width, height, 0, format, GL_UNSIGNED_BYTE, bytes);

        stbi_image_free(bytes);
        std::cout << "Texture(" << path << "): " << width << " x " << height << ", channels = " << channels << ", ID = " << ID << std::endl;
    }

    ~Texture()
    {
        glDeleteTextures(1, &ID);
        std::cout << "~Texture(): deleted ID = " << ID << std::endl;
    }

    void Bind(GLuint unit)
    {
        glActiveTexture(GL_TEXTURE0 + unit);
        glBindTexture(GL_TEXTURE_2D, ID);
    }

    void SetWrap(GLint mode)
    {
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, mode);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, mode);
    }
};

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(960, 480, "Wrap by hand", nullptr, nullptr);
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
        -1.0f, -1.0f,   -1.0f, -1.0f,
         1.0f, -1.0f,    2.0f, -1.0f,
         1.0f,  1.0f,    2.0f,  2.0f,
        -1.0f,  1.0f,   -1.0f,  2.0f
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
        "uniform int mode;\n"
        "vec2 Wrap(vec2 uv)\n"
        "{\n"
        "    if (mode == 1)\n"
        "        return uv - floor(uv);\n"
        "    if (mode == 2)\n"
        "        return 1.0 - abs(mod(uv, 2.0) - 1.0);\n"
        "    if (mode == 3)\n"
        "        return clamp(uv, 0.0, 1.0);\n"
        "    return uv;\n"
        "}\n"
        "void main()\n"
        "{\n"
        "    FragColor = texture(tex0, Wrap(texCoord));\n"
        "}\n";

    GLuint shaderProgram = CreateShader(vertexShader, fragmentShader);
    glUseProgram(shaderProgram);
    glUniform1i(glGetUniformLocation(shaderProgram, "tex0"), 0);
    GLint modeLoc = glGetUniformLocation(shaderProgram, "mode");
    GLint cardModes[] = { GL_REPEAT, GL_MIRRORED_REPEAT, GL_CLAMP_TO_EDGE };
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f);

    {
        Texture letter("res/letter.png");
        letter.Bind(0);

        while (!glfwWindowShouldClose(window))
        {
            if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
                glfwSetWindowShouldClose(window, true);

            glViewport(0, 0, 960, 480);
            glClear(GL_COLOR_BUFFER_BIT);
            glBindVertexArray(vao);
            for (int i = 0; i < 3; i++)
            {
                glViewport(i * 320 + 4, 244, 312, 232);
                letter.SetWrap(cardModes[i]);
                glUniform1i(modeLoc, 0);
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

                glViewport(i * 320 + 4, 4, 312, 232);
                letter.SetWrap(GL_CLAMP_TO_EDGE);
                glUniform1i(modeLoc, i + 1);
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
            }

            glfwSwapBuffers(window);
            glfwPollEvents();
        }
        std::cout << "loop ended (Escape)" << std::endl;
    }

    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
