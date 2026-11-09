#include <iostream>
#include <string>
#include <algorithm>
#include <utility>

namespace reverse_string
{
    std::string naive(std::string input)
    {
        std::string reversed;
        int length = input.length();
        for (int i = length - 1; i >= 0; i--)
            reversed += input[i];
        return reversed;
    }

    std::string in_place(std::string input)
    {
        if (input.empty())
            return input;
        size_t left = 0;
        size_t right = input.length() - 1;
        while (left < right)
        {
            char temp = input[left];
            input[left] = input[right];
            input[right] = temp;
            left++;
            right--;
        }
        return input;
    }

    std::string with_swap(std::string input)
    {
        if (input.empty())
            return input;
        size_t left = 0;
        size_t right = input.length() - 1;
        while (left < right)
            std::swap(input[left++], input[right--]);
        return input;
    }

    std::string reverse_string(std::string input)
    {
        std::reverse(input.begin(), input.end());
        return input;
    }
}

int main()
{
    std::string words[3] = { "stressed", "racecar", "" };
    for (const std::string& w : words)
    {
        std::cout << "\"" << w << "\" -> naive \"" << reverse_string::naive(w)
                  << "\", in_place \"" << reverse_string::in_place(w)
                  << "\", with_swap \"" << reverse_string::with_swap(w)
                  << "\", std::reverse \"" << reverse_string::reverse_string(w) << "\"" << std::endl;
    }
    size_t zero = 0;
    std::cout << "why check empty(): size_t 0 - 1 = " << zero - 1 << std::endl;
    return 0;
}
