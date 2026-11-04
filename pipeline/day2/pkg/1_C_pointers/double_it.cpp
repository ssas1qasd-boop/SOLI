#include <iostream>

void doubleIt(int* number)
{
    *number = *number * 2;
}

int main()
{
    int score = 21;
    std::cout << "before: " << score << std::endl;
    doubleIt(&score);
    std::cout << "after:  " << score << std::endl;
    std::cin.get();
}
