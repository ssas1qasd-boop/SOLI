#include <iostream>
#include <cmath>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

struct Matrix4f
{
    float m[4][4];
};

Matrix4f Identity()
{
    return { { { 1, 0, 0, 0 }, { 0, 1, 0, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 1 } } };
}

Matrix4f RotationX(float a)
{
    Matrix4f r = Identity();
    r.m[1][1] = std::cos(a); r.m[1][2] = -std::sin(a);
    r.m[2][1] = std::sin(a); r.m[2][2] = std::cos(a);
    return r;
}

Matrix4f RotationY(float a)
{
    Matrix4f r = Identity();
    r.m[0][0] = std::cos(a); r.m[0][2] = std::sin(a);
    r.m[2][0] = -std::sin(a); r.m[2][2] = std::cos(a);
    return r;
}

Matrix4f RotationZ(float a)
{
    Matrix4f r = Identity();
    r.m[0][0] = std::cos(a); r.m[0][1] = -std::sin(a);
    r.m[1][0] = std::sin(a); r.m[1][1] = std::cos(a);
    return r;
}

Matrix4f Scale(float s)
{
    Matrix4f r = Identity();
    r.m[0][0] = s; r.m[1][1] = s; r.m[2][2] = s;
    return r;
}

Matrix4f Translation(float x, float y, float z)
{
    Matrix4f r = Identity();
    r.m[0][3] = x; r.m[1][3] = y; r.m[2][3] = z;
    return r;
}

Matrix4f operator*(const Matrix4f& a, const Matrix4f& b)
{
    Matrix4f r;
    for (int row = 0; row < 4; row++)
        for (int col = 0; col < 4; col++)
        {
            r.m[row][col] = 0;
            for (int k = 0; k < 4; k++)
                r.m[row][col] += a.m[row][k] * b.m[k][col];
        }
    return r;
}

void Apply(const char* name, const Matrix4f& M, float x, float y, float z)
{
    float in[4] = { x, y, z, 1 }, out[4];
    for (int row = 0; row < 4; row++)
    {
        out[row] = 0;
        for (int k = 0; k < 4; k++)
            out[row] += M.m[row][k] * in[k];
    }
    std::cout << name << " (" << std::round(out[0] * 1000) / 1000 + 0.0f << ", " << std::round(out[1] * 1000) / 1000 + 0.0f << ", " << std::round(out[2] * 1000) / 1000 + 0.0f << ")" << std::endl;
}

int main()
{
    float a = glm::radians(90.0f);
    Matrix4f chain = RotationZ(a) * RotationY(a) * RotationX(a);
    glm::mat4 g = glm::rotate(glm::mat4(1.0f), a, glm::vec3(0, 0, 1)) * glm::rotate(glm::mat4(1.0f), a, glm::vec3(0, 1, 0)) * glm::rotate(glm::mat4(1.0f), a, glm::vec3(1, 0, 0));
    float worst = 0;
    for (int row = 0; row < 4; row++)
        for (int col = 0; col < 4; col++)
            worst = std::fmax(worst, std::fabs(chain.m[row][col] - g[col][row]));
    std::cout << "chain Rz * Ry * Rx vs glm: biggest difference " << worst << std::endl;
    Apply("chain * (0, 1, 0) =", chain, 0, 1, 0);

    Apply("RotationZ(90) * (3, 0, 0)          =", RotationZ(a), 3, 0, 0);
    Matrix4f aroundSelf = Translation(3, 0, 0) * RotationZ(a) * Translation(-3, 0, 0);
    Apply("T(3) R T(-3) * centre (3, 0, 0)    =", aroundSelf, 3, 0, 0);
    Apply("T(3) R T(-3) * corner (4, 0, 0)    =", aroundSelf, 4, 0, 0);
    return 0;
}
