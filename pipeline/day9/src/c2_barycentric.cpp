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

struct Corner
{
    float x, y;
    float r, g, b;
};

void CheckPixel(const Corner* t, int px, int py)
{
    float x = (px + 0.5f) / 640.0f * 2.0f - 1.0f;
    float y = (py + 0.5f) / 480.0f * 2.0f - 1.0f;
    float A = (t[1].x - t[0].x) * (t[2].y - t[0].y) - (t[2].x - t[0].x) * (t[1].y - t[0].y);
    float alpha = ((t[1].x - x) * (t[2].y - y) - (t[2].x - x) * (t[1].y - y)) / A;
    float beta = ((x - t[0].x) * (t[2].y - t[0].y) - (t[2].x - t[0].x) * (y - t[0].y)) / A;
    float gamma = 1.0f - alpha - beta;
    float r = alpha * t[0].r + beta * t[1].r + gamma * t[2].r;
    float g = alpha * t[0].g + beta * t[1].g + gamma * t[2].g;
    float b = alpha * t[0].b + beta * t[1].b + gamma * t[2].b;

    unsigned char gpu[4];
    glReadPixels(px, py, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, gpu);
    std::cout << "pixel (" << px << ", " << py << "): alpha = " << alpha << ", beta = " << beta << ", gamma = " << gamma << std::endl;
    if (alpha < 0 || beta < 0 || gamma < 0)
        std::cout << "   outside the triangle, GPU color = " << (int)gpu[0] << " " << (int)gpu[1] << " " << (int)gpu[2] << std::endl;
    else
        std::cout << "   CPU color = " << (int)(r * 255 + 0.5f) << " " << (int)(g * 255 + 0.5f) << " " << (int)(b * 255 + 0.5f)
                  << "   GPU color = " << (int)gpu[0] << " " << (int)gpu[1] << " " << (int)gpu[2] << std::endl;
}

int main()
{
    if (!glfwInit())
        return -1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(640, 480, "Barycentric", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
        return -1;

    Corner triangle[3] = {
        { -0.8f, -0.8f,   1.0f, 0.0f, 0.0f },
        {  0.8f, -0.8f,   0.0f, 1.0f, 0.0f },
        {  0.0f,  0.8f,   0.0f, 0.0f, 1.0f }
    };

    GLuint vao, vbo;
    glGenVertexArrays(1, &vao);
    glBindVertexArray(vao);
    glGenBuffers(1, &vbo);
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(triangle), triangle, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(Corner), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(Corner), (void*)(2 * sizeof(float)));
    glEnableVertexAttribArray(1);

    std::string vertexShader =
        "#version 330 core\n"
        "layout (location = 0) in vec2 aPos;\n"
        "layout (location = 1) in vec3 aColor;\n"
        "out vec3 color;\n"
        "void main()\n"
        "{\n"
        "    gl_Position = vec4(aPos, 0.0, 1.0);\n"
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

    int frame = 0;
    while (!glfwWindowShouldClose(window))
    {
        glClear(GL_COLOR_BUFFER_BIT);
        glDrawArrays(GL_TRIANGLES, 0, 3);

        if (frame == 0)
        {
            CheckPixel(triangle, 320, 240);
            CheckPixel(triangle, 200, 100);
            CheckPixel(triangle, 60, 400);
            std::cout << "glGetError() = " << glGetError() << std::endl;
        }
        frame++;

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteProgram(shaderProgram);
    glfwTerminate();
    return 0;
}
