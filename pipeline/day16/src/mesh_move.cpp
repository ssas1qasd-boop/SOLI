#include <iostream>
#include <cmath>

struct Vec3
{
    float x, y, z;
};

float Distance(Vec3 a, Vec3 b)
{
    return std::sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y) + (a.z - b.z) * (a.z - b.z));
}

void Edges(const char* name, Vec3* v)
{
    std::cout << name << ": edges " << Distance(v[0], v[1]) << ", " << Distance(v[1], v[2]) << ", " << Distance(v[2], v[0]) << std::endl;
}

int main()
{
    Vec3 mesh[3] = { { 0, 0, 0 }, { 3, 0, 0 }, { 0, 4, 0 } };
    Edges("original    ", mesh);

    Vec3 all[3];
    for (int i = 0; i < 3; i++)
        all[i] = { mesh[i].x + 2, mesh[i].y + 1, mesh[i].z - 5 };
    Edges("move all 3  ", all);

    Vec3 one[3] = { mesh[0], mesh[1], mesh[2] };
    one[1] = { one[1].x + 2, one[1].y + 1, one[1].z - 5 };
    Edges("move only #1", one);
    return 0;
}
