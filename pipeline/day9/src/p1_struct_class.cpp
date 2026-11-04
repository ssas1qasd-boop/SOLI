#include <iostream>

struct PlayerS
{
    int x, y;
    int speed;

    void Move(int xa, int ya)
    {
        x += xa * speed;
        y += ya * speed;
    }
};

class PlayerC
{
public:
    int x, y;
    int speed;

    void Move(int xa, int ya)
    {
        x += xa * speed;
        y += ya * speed;
    }
};

struct Vec2
{
    float x, y;

    void Add(const Vec2& other)
    {
        x += other.x;
        y += other.y;
    }
};

int main()
{
    PlayerS s;
    s.x = 0; s.y = 0; s.speed = 2;
    s.Move(1, -1);

    PlayerC c;
    c.x = 0; c.y = 0; c.speed = 2;
    c.Move(1, -1);

    std::cout << "struct: x = " << s.x << ", y = " << s.y << ", sizeof = " << sizeof(PlayerS) << std::endl;
    std::cout << "class:  x = " << c.x << ", y = " << c.y << ", sizeof = " << sizeof(PlayerC) << std::endl;

    Vec2 position = { 1.0f, 2.0f };
    Vec2 velocity = { 0.5f, -1.0f };
    position.Add(velocity);
    position.Add(velocity);
    std::cout << "position after 2 Add: (" << position.x << ", " << position.y << ")" << std::endl;
    std::cout << "sizeof(Vec2) = " << sizeof(Vec2) << " bytes" << std::endl;
    return 0;
}
