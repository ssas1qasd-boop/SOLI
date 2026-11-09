#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <unordered_map>

struct CityRecord
{
    std::string Name;
    int Population;

    bool operator<(const CityRecord& other) const
    {
        return Population < other.Population;
    }
};

int main()
{
    std::vector<int> values = { 1, 2, 3, 4, 5 };
    std::cout << "iterator:        ";
    for (std::vector<int>::iterator it = values.begin(); it != values.end(); it++)
        std::cout << *it << " ";
    std::cout << std::endl << "reverse_iterator:";
    for (std::vector<int>::reverse_iterator it = values.rbegin(); it != values.rend(); it++)
        std::cout << " " << *it;
    std::cout << std::endl;

    for (std::vector<int>::iterator it = values.begin(); it != values.end(); )
    {
        if (*it % 2 == 0)
            it = values.erase(it);
        else
            it++;
    }
    std::cout << "after erasing even values:";
    for (int value : values)
        std::cout << " " << value;
    std::cout << std::endl;

    using ScoreMap = std::unordered_map<std::string, int>;
    ScoreMap map;
    map["Cherno"] = 5;
    map["C++"] = 2;
    int total = 0;
    for (ScoreMap::const_iterator it = map.begin(); it != map.end(); it++)
        total += it->second;
    std::cout << "sum of values with const_iterator = " << total << ", map[\"Cherno\"] = " << map["Cherno"] << std::endl;

    std::map<CityRecord, int> founded;
    founded[{ "Berlin", 3500000 }] = 1237;
    founded[{ "Paris", 2100000 }] = 259;
    founded[{ "Madrid", 3500000 }] = 865;
    std::cout << "std::map<CityRecord, int> after 3 inserts: size " << founded.size() << std::endl;
    for (const auto& [city, year] : founded)
        std::cout << "  " << city.Name << " " << city.Population << " -> " << year << std::endl;
    return 0;
}
