// exercism C++ track: Raindrops
#include <iostream>
#include <string>

namespace raindrops
{
    std::string convert(int drops)
    {
        std::string sound = "";
        if (drops % 3 == 0)
            sound += "Pling";
        if (drops % 5 == 0)
            sound += "Plang";
        if (drops % 7 == 0)
            sound += "Plong";
        if (sound.empty())
            sound = std::to_string(drops);
        return sound;
    }
}

void check(int drops, const std::string& expected)
{
    std::string got = raindrops::convert(drops);
    std::cout << drops << " -> " << got
              << (got == expected ? "   PASS" : "   FAIL") << std::endl;
}

int main()
{
    check(1, "1");
    check(3, "Pling");
    check(10, "Plang");
    check(14, "Plong");
    check(15, "PlingPlang");
    check(105, "PlingPlangPlong");
    check(34, "34");
    return 0;
}
