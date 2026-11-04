#include <iostream>
#include <chrono>

struct Vector3
{
    float x, y, z;

    Vector3()
        : x(10), y(11), z(12)
    {
    }
};

const int N = 100;

double Now()
{
    return std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now().time_since_epoch()).count();
}

unsigned char* LoadTexture(int width, int height)
{
    unsigned char* pixels = new unsigned char[width * height * 4];
    pixels[0] = 200;
    std::cout << "LoadTexture: " << width * height * 4 / (1024 * 1024) << " MB on the heap" << std::endl;
    return pixels;
}

int main()
{
    float sum = 0.0f;

    double t0 = Now();
    for (int i = 0; i < N; i++)
    {
        Vector3 v;
        sum += v.x;
    }
    double t1 = Now();
    for (int i = 0; i < N; i++)
    {
        Vector3* v = new Vector3();
        sum += v->x;
        delete v;
    }
    double t2 = Now();

    std::cout << N << " x stack Vector3: " << (t1 - t0) / N << " ns each" << std::endl;
    std::cout << N << " x new + delete Vector3: " << (t2 - t1) / N << " ns each" << std::endl;
    std::cout << "heap / stack = " << (t2 - t1) / (t1 - t0) << std::endl;
    std::cout << "sum = " << sum << std::endl;

    unsigned char* texture = LoadTexture(2048, 2048);
    std::cout << "back in main: texture[0] = " << (int)texture[0] << " (still alive)" << std::endl;
    delete[] texture;
    std::cout << "delete[] texture: 16 MB returned" << std::endl;
    return 0;
}
