#include <iostream>
#include <cstring>

void Swap(int* a, int* b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

void SetToZero(int* p)
{
    if (p != nullptr)
        *p = 0;
}

void MakeText(char** out, int size)
{
    *out = new char[size];
    memset(*out, 'x', size - 1);
    (*out)[size - 1] = 0;
}

int Sum(const int* values, int count)
{
    int total = 0;
    for (int i = 0; i < count; i++)
        total += *(values + i);
    return total;
}

void check(const char* question, bool ok)
{
    std::cout << question << (ok ? "   PASS" : "   FAIL") << std::endl;
}

int main()
{
    int a = 3, b = 7;
    Swap(&a, &b);
    check("Swap(&a, &b): a = 7, b = 3", a == 7 && b == 3);

    int n = 5;
    SetToZero(&n);
    SetToZero(nullptr);
    check("SetToZero(&n): n = 0", n == 0);

    char* text = nullptr;
    MakeText(&text, 4);
    check("MakeText(&text, 4): text = xxx", text != nullptr && strcmp(text, "xxx") == 0);
    delete[] text;

    int values[4] = { 1, 2, 3, 4 };
    check("Sum(values, 4) = 10", Sum(values, 4) == 10);
    return 0;
}
