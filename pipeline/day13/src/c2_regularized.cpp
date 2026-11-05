#include <iostream>
#include <vector>
#include <algorithm>

struct Interval
{
    float a, b;
};

std::vector<Interval> Intersect(const std::vector<Interval>& A, const std::vector<Interval>& B)
{
    std::vector<Interval> out;
    for (const Interval& p : A)
        for (const Interval& q : B)
        {
            float a = std::max(p.a, q.a), b = std::min(p.b, q.b);
            if (a <= b)
                out.push_back({ a, b });
        }
    return out;
}

std::vector<Interval> Regularize(const std::vector<Interval>& A)
{
    std::vector<Interval> out;
    for (const Interval& p : A)
        if (p.b > p.a)
            out.push_back(p);
    return out;
}

void Print(const char* name, const std::vector<Interval>& A)
{
    float length = 0.0f;
    std::cout << name << ": " << A.size() << " piece(s)";
    for (const Interval& p : A)
    {
        std::cout << " [" << p.a << ", " << p.b << "]";
        length += p.b - p.a;
    }
    std::cout << ", length = " << length << std::endl;
}

int main()
{
    std::vector<Interval> A = { { 0, 2 } };
    std::vector<Interval> B = { { 1, 3 } };
    std::vector<Interval> C = { { 2, 4 } };
    Print("A inter B (overlap)  ", Intersect(A, B));
    Print("A inter C (touching) ", Intersect(A, C));
    Print("regularized A inter C", Regularize(Intersect(A, C)));
    std::vector<Interval> plate = { { 0, 10 } };
    std::vector<Interval> notHole = { { -100, 4 }, { 6, 100 } };
    Print("plate minus hole     ", Regularize(Intersect(plate, notHole)));
    return 0;
}
