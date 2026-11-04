#include <iostream>
#include <vector>

struct Point
{
    float x, y;
};

void addPoint(std::vector<Point>& points, float x, float y)
{
    points.push_back({ x, y });
}

void printPoints(const std::vector<Point>& points)
{
    std::cout << points.size() << " points:" << std::endl;
    for (const Point& p : points)
        std::cout << "  (" << p.x << ", " << p.y << ")" << std::endl;
}

int main()
{
    std::vector<Point> points;
    addPoint(points, 0, 0);
    addPoint(points, 100, 0);
    addPoint(points, 100, 50);
    printPoints(points);

    points.pop_back();
    printPoints(points);
    std::cin.get();
}
