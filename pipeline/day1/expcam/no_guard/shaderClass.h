
#include <glad/glad.h>

class Shader
{
public:
    GLuint ID;
    Shader(const char* vertexSource, const char* fragmentSource);
    void Activate();
    void Delete();
};

