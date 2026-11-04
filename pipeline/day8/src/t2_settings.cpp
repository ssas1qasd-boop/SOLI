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

static unsigned int MakeTexture(const unsigned char* pixels, int size, int filter, int wrap)
{
    unsigned int id;
    glGenTextures(1, &id);
    glBindTexture(GL_TEXTURE_2D, id);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filter);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels);
    return id;
}

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(640, 480, "Texture Settings", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    unsigned char pixels[4 * 4 * 4];
    for (int row = 0; row < 4; row++)
    {
        for (int col = 0; col < 4; col++)
        {
            unsigned char* p = &pixels[(row * 4 + col) * 4];
            bool dark = (row + col) % 2 == 0;
            p[0] = dark ? 40 : 250;
            p[1] = dark ? 90 : 200;
            p[2] = dark ? 200 : 60;
            p[3] = 255;
        }
    }

    unsigned int sharp = MakeTexture(pixels, 4, GL_NEAREST, GL_REPEAT);
    unsigned int smooth = MakeTexture(pixels, 4, GL_LINEAR, GL_CLAMP_TO_EDGE);
    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, sharp);
    glActiveTexture(GL_TEXTURE1);
    glBindTexture(GL_TEXTURE_2D, smooth);

    float positions[16] = {
        -0.4f, -0.4f, 0.0f, 0.0f,
         0.4f, -0.4f, 1.0f, 0.0f,
         0.4f,  0.4f, 1.0f, 1.0f,
        -0.4f,  0.4f, 0.0f, 1.0f
    };

    unsigned int indices[6] = {
        0, 1, 2,
        2, 3, 0
    };

    unsigned int vao;
    glGenVertexArrays(1, &vao);
    glBindVertexArray(vao);

    unsigned int buffer;
    glGenBuffers(1, &buffer);
    glBindBuffer(GL_ARRAY_BUFFER, buffer);
    glBufferData(GL_ARRAY_BUFFER, 16 * sizeof(float), positions, GL_STATIC_DRAW);

    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 4, 0);
    glEnableVertexAttribArray(1);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 4, (const void*)(sizeof(float) * 2));

    unsigned int ibo;
    glGenBuffers(1, &ibo);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 6 * sizeof(unsigned int), indices, GL_STATIC_DRAW);

    std::string vertexShader =
        "#version 330 core\n"
        "\n"
        "layout(location = 0) in vec4 position;\n"
        "layout(location = 1) in vec2 texCoord;\n"
        "\n"
        "uniform vec2 u_Offset;\n"
        "uniform float u_Repeat;\n"
        "out vec2 v_TexCoord;\n"
        "\n"
        "void main()\n"
        "{\n"
        "    gl_Position = vec4(position.xy + u_Offset, 0.0, 1.0);\n"
        "    v_TexCoord = texCoord * u_Repeat;\n"
        "}\n";

    std::string fragmentShader =
        "#version 330 core\n"
        "\n"
        "layout(location = 0) out vec4 color;\n"
        "\n"
        "in vec2 v_TexCoord;\n"
        "uniform sampler2D u_Texture;\n"
        "\n"
        "void main()\n"
        "{\n"
        "    color = texture(u_Texture, v_TexCoord);\n"
        "}\n";

    unsigned int shader = CreateShader(vertexShader, fragmentShader);
    glUseProgram(shader);
    int textureLocation = glGetUniformLocation(shader, "u_Texture");
    int offsetLocation = glGetUniformLocation(shader, "u_Offset");
    int repeatLocation = glGetUniformLocation(shader, "u_Repeat");

    int frame = 0;
    while (!glfwWindowShouldClose(window))
    {
        glClear(GL_COLOR_BUFFER_BIT);

        // top left: slot 0 (sharp), coordinates 0..1
        glUniform1i(textureLocation, 0);
        glUniform2f(offsetLocation, -0.5f, 0.5f);
        glUniform1f(repeatLocation, 1.0f);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);

        // top right: slot 1 (smooth), coordinates 0..1
        glUniform1i(textureLocation, 1);
        glUniform2f(offsetLocation, 0.5f, 0.5f);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);

        // bottom left: slot 0 (repeat), coordinates 0..2
        glUniform1i(textureLocation, 0);
        glUniform2f(offsetLocation, -0.5f, -0.5f);
        glUniform1f(repeatLocation, 2.0f);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);

        // bottom right: slot 1 (clamp to edge), coordinates 0..2
        glUniform1i(textureLocation, 1);
        glUniform2f(offsetLocation, 0.5f, -0.5f);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);

        if (frame == 0)
            std::cout << "frame 0 drawn, glGetError() = " << glGetError() << std::endl;
        frame++;

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteTextures(1, &sharp);
    glDeleteTextures(1, &smooth);
    glDeleteProgram(shader);
    glfwTerminate();
    return 0;
}
