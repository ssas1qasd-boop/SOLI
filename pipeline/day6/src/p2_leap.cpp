// exercism C++ track: Leap
#include <iostream>

namespace leap
{
    bool is_leap_year(int year)
    {
        return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
    }
}

void check(int year, bool expected)
{
    bool got = leap::is_leap_year(year);
    std::cout << year << ": " << (got ? "leap" : "not leap")
              << (got == expected ? "   PASS" : "   FAIL") << std::endl;
}

int main()
{
    check(2015, false);
    check(1996, true);
    check(2100, false);
    check(2000, true);
    check(1900, false);
    check(2024, true);
    return 0;
}
