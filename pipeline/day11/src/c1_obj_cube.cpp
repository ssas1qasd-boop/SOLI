#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <set>
#include <algorithm>

struct Vec3
{
    float x, y, z;
};

Vec3 Sub(Vec3 a, Vec3 b)
{
    return { a.x - b.x, a.y - b.y, a.z - b.z };
}

Vec3 Cross(Vec3 a, Vec3 b)
{
    return { a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x };
}

float Dot(Vec3 a, Vec3 b)
{
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

int main()
{
    std::ofstream obj("cube.obj");
    obj << "# cube from the video: bottom z = 0, top z = 2\n";
    obj << "v 1 -1 0\nv 1 1 0\nv -1 1 0\nv -1 -1 0\n";
    obj << "v 1 -1 2\nv 1 1 2\nv -1 1 2\nv -1 -1 2\n";
    obj << "f 1 4 3 2\nf 5 6 7 8\nf 1 5 8 4\nf 2 3 7 6\nf 1 2 6 5\nf 4 8 7 3\n";
    obj.close();

    std::vector<Vec3> v;
    std::vector<std::vector<int>> faces;
    std::ifstream in("cube.obj");
    std::string line;
    while (std::getline(in, line))
    {
        std::istringstream words(line);
        std::string tag;
        words >> tag;
        if (tag == "v")
        {
            Vec3 p;
            words >> p.x >> p.y >> p.z;
            v.push_back(p);
        }
        else if (tag == "f")
        {
            std::vector<int> f;
            int index;
            while (words >> index)
                f.push_back(index - 1);
            faces.push_back(f);
        }
    }
    std::cout << "read cube.obj: " << v.size() << " vertices, " << faces.size() << " faces" << std::endl;

    Vec3 center = { 0.0f, 0.0f, 1.0f };
    for (int i = 0; i < (int)faces.size(); i++)
    {
        std::vector<int>& f = faces[i];
        Vec3 n = Cross(Sub(v[f[1]], v[f[0]]), Sub(v[f[2]], v[f[0]]));
        Vec3 mid = { 0.0f, 0.0f, 0.0f };
        for (int k : f)
        {
            mid.x += v[k].x / f.size();
            mid.y += v[k].y / f.size();
            mid.z += v[k].z / f.size();
        }
        float out = Dot(n, Sub(mid, center));
        std::cout << "face " << i + 1 << ": normal (" << n.x << ", " << n.y << ", " << n.z << ")" << (out > 0 ? "  outward" : "  INWARD") << std::endl;
    }

    std::set<std::pair<int, int>> edges;
    for (std::vector<int>& f : faces)
        for (int k = 0; k < (int)f.size(); k++)
            edges.insert({ std::min(f[k], f[(k + 1) % f.size()]), std::max(f[k], f[(k + 1) % f.size()]) });
    int V = v.size(), E = edges.size(), F = faces.size();
    std::cout << "V = " << V << ", E = " << E << ", F = " << F << ", V - E + F = " << V - E + F << std::endl;
    return 0;
}
