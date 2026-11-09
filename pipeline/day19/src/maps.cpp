#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <cstdint>

struct CityRecord
{
    std::string Name;
    uint64_t Population;
    double Latitude, Longitude;
};

int main()
{
    std::vector<CityRecord> cities;
    cities.push_back({ "Melbourne", 5000000, 0.0, 0.0 });
    cities.push_back({ "Lol-town", 5000000, 0.0, 0.0 });
    cities.push_back({ "Berlin", 3500000, 0.0, 0.0 });
    cities.push_back({ "Paris", 2100000, 0.0, 0.0 });
    cities.push_back({ "London", 8900000, 0.0, 0.0 });
    int comparisons = 0;
    for (const CityRecord& city : cities)
    {
        comparisons++;
        if (city.Name == "London")
            break;
    }
    std::cout << "vector: found London after " << comparisons << " string comparisons" << std::endl;

    std::map<std::string, CityRecord> cityMap;
    for (const CityRecord& city : cities)
        cityMap[city.Name] = city;
    std::cout << "cityMap[\"London\"].Population = " << cityMap["London"].Population << std::endl;

    std::cout << "std::map order:";
    for (const auto& [name, city] : cityMap)
        std::cout << " " << name;
    std::cout << std::endl;

    std::cout << "size before cityMap[\"Cairo\"] = " << cityMap.size();
    uint64_t cairo = cityMap["Cairo"].Population;
    std::cout << ", after = " << cityMap.size() << " (Cairo population " << cairo << ")" << std::endl;

    if (cityMap.find("Tokyo") == cityMap.end())
        std::cout << "find(\"Tokyo\") == end(): not there, nothing inserted, size " << cityMap.size() << std::endl;
    try
    {
        std::cout << cityMap.at("Tokyo").Population << std::endl;
    }
    catch (const std::out_of_range& e)
    {
        std::cout << "at(\"Tokyo\") threw std::out_of_range" << std::endl;
    }

    cityMap.erase("Cairo");
    std::cout << "after erase(\"Cairo\"): size " << cityMap.size() << std::endl;

    std::unordered_map<std::string, CityRecord> hashMap(cityMap.begin(), cityMap.end());
    std::cout << "unordered_map has " << hashMap.size() << " cities, Berlin = " << hashMap.at("Berlin").Population << std::endl;
    return 0;
}
