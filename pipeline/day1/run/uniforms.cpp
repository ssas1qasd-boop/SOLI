// Code from "Uniforms in OpenGL" (The Cherno): a square whose color comes from a uniform.
#include "common.h"

static const char* vs = R"(#version 330 core
layout(location = 0) in vec4 position;
void main() { gl_Position = position; })";

static const char* fs = R"(#version 330 core
layout(location = 0) out vec4 color;
uniform vec4 u_Color;
void main() { color = u_Color; })";

int main()
{
    const int W = 640, H = 480;
    GLFWwindow* window = MakeWindow(W, H, "Uniforms");

    float positions[] = { -0.5f,-0.5f,  0.5f,-0.5f,  0.5f,0.5f,  -0.5f,0.5f };
    unsigned int indices[] = { 0,1,2,  2,3,0 };

    unsigned int vao, vbo, ibo;
    glGenVertexArrays(1, &vao); glBindVertexArray(vao);
    glGenBuffers(1, &vbo); glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(positions), positions, GL_STATIC_DRAW);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), 0);
    glGenBuffers(1, &ibo); glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

    unsigned int shader = CreateShader(vs, fs);
    glUseProgram(shader);

    // ---- Code 2: get the location ----
    int location = glGetUniformLocation(shader, "u_Color");
    std::cout << "glGetUniformLocation(\"u_Color\") = " << location << "\n";
    int wrong = glGetUniformLocation(shader, "u_Colour");   // typo on purpose
    std::cout << "glGetUniformLocation(\"u_Colour\") = " << wrong << "   <- typo, not found\n";

    // ---- Code 3: one fixed color ----
    glClear(GL_COLOR_BUFFER_BIT);
    glUniform4f(location, 0.2f, 0.3f, 0.8f, 1.0f);
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);
    SaveScreenshot("out/uni_fixed.ppm", W, H);
    glfwSwapBuffers(window);

    // ---- Code 4: animation; save some frames ----
    float r = 0.0f;
    float increment = 0.05f;
    for (int frame = 0; frame <= 42; frame++)
    {
        glClear(GL_COLOR_BUFFER_BIT);
        glUniform4f(location, r, 0.3f, 0.8f, 1.0f);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);

        if (frame % 7 == 0) {
            char name[64]; snprintf(name, 64, "out/uni_f%02d.ppm", frame);
            SaveScreenshot(name, W, H);
            std::cout << "frame " << frame << "  r = " << r << "\n";
        }

        if (r > 1.0f)       increment = -0.05f;
        else if (r < 0.0f)  increment =  0.05f;
        r += increment;

        glfwSwapBuffers(window);
        glfwPollEvents();
    }
    glDeleteProgram(shader);
    glfwTerminate();
}
