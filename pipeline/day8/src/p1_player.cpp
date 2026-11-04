#include <iostream>

class Player
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

void Move(Player& player, int xa, int ya)
{
    player.x += xa * player.speed;
    player.y += ya * player.speed;
}

int main()
{
    Player player;
    player.x = 0;
    player.y = 0;
    player.speed = 2;
    std::cout << "start:              x = " << player.x << ", y = " << player.y << std::endl;

    player.Move(1, -1);
    std::cout << "player.Move(1, -1): x = " << player.x << ", y = " << player.y << std::endl;

    Move(player, 1, -1);
    std::cout << "Move(player, 1, -1): x = " << player.x << ", y = " << player.y << std::endl;

    Player enemy;
    enemy.x = 10;
    enemy.y = 10;
    enemy.speed = 5;
    enemy.Move(-1, 0);
    std::cout << "enemy:              x = " << enemy.x << ", y = " << enemy.y << std::endl;
    std::cout << "player still:       x = " << player.x << ", y = " << player.y << std::endl;

    std::cout << "sizeof(Player) = " << sizeof(Player) << " bytes" << std::endl;
    std::cout << "&player       = " << &player << std::endl;
    std::cout << "&player.x     = " << &player.x << std::endl;
    std::cout << "&player.y     = " << &player.y << std::endl;
    std::cout << "&player.speed = " << &player.speed << std::endl;
    return 0;
}
