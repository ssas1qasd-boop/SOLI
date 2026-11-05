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

class Texture
{
public:
    GLuint id;

    Texture(unsigned char r, unsigned char g, unsigned char b)
    {
        unsigned char pixels[2 * 2 * 3] = { r, g, b,   255, 255, 255,   255, 255, 255,   r, g, b };
        glGenTextures(1, &id);
        glBindTexture(GL_TEXTURE_2D, id);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2, 2, 0, GL_RGB, GL_UNSIGNED_BYTE, pixels);
        std::cout << "Texture() made id " << id << std::endl;
    }

    Texture(const Texture& other) = delete;

    ~Texture()
    {
        std::cout << "~Texture() deletes id " << id << std::endl;
        glDeleteTextures(1, &id);
    }

    void Bind() const
    {
        glBindTexture(GL_TEXTURE_2D, id);
    }
};

void Describe(const Texture& texture)
{
    std::cout << "Describe: id " << texture.id << ", glIsTexture = " << (int)glIsTexture(texture.id) << std::endl;
}

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(960, 480, "Texture reference", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    {
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

    Texture red(220, 38, 38);
    Texture blue(37, 99, 235);
    Describe(blue);
    std::cout << "after Describe: red glIsTexture = " << (int)glIsTexture(red.id) << ", blue glIsTexture = " << (int)glIsTexture(blue.id) << std::endl;
    Texture* textures[2] = { &red, &blue };

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
            textures[i]->Bind();
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shaderProgram);
    }
    glfwTerminate();
    return 0;
}
