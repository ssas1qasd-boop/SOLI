#include <iostream>
#include <cmath>

int main()
{
    float px[3] = { 1, 0, -1 };
    float py[3] = { 0, 1, 0 };

    std::cout << "turn 30:";
    for (int i = 0; i < 3; i++)
    {
        float x = px[i] * std::cos(0.5236f) - py[i] * std::sin(0.5236f);
        float y = px[i] * std::sin(0.5236f) + py[i] * std::cos(0.5236f);
        std::cout << " (" << std::round(x * 100) / 100 + 0.0f << ", " << std::round(y * 100) / 100 + 0.0f << ")";
    }
    std::cout << std::endl;

    std::cout << "turn 60:";
    for (int i = 0; i < 3; i++)
    {
        float x = px[i] * std::cos(1.0472f) - py[i] * std::sin(1.0472f);
        float y = px[i] * std::sin(1.0472f) + py[i] * std::cos(1.0472f);
        std::cout << " (" << std::round(x * 100) / 100 + 0.0f << ", " << std::round(y * 100) / 100 + 0.0f << ")";
    }
    std::cout << std::endl;

    std::cout << "turn 90:";
    for (int i = 0; i < 3; i++)
    {
        float x = px[i] * std::cos(1.5708f) - py[i] * std::sin(1.5708f);
        float y = px[i] * std::sin(1.5708f) + py[i] * std::cos(1.5708f);
        std::cout << " (" << std::round(x * 100) / 100 + 0.0f << ", " << std::round(y * 100) / 100 + 0.0f << ")";
    }
    std::cout << std::endl;
    return 0;
}
