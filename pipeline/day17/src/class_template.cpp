#include <iostream>
#include <string>

template<typename T, int N = 4>
class Stack
{
private:
    T m_Items[N];
    int m_Count = 0;

public:
    bool Push(const T& item);
    T Pop();
    int Size() const { return m_Count; }
    int Capacity() const { return N; }
};

template<typename T, int N>
bool Stack<T, N>::Push(const T& item)
{
    if (m_Count == N)
        return false;
    m_Items[m_Count++] = item;
    return true;
}

template<typename T, int N>
T Stack<T, N>::Pop()
{
    return m_Items[--m_Count];
}

int main()
{
    Stack<int> numbers;
    for (int i = 1; i <= 5; i++)
        std::cout << "Push(" << i << "): " << (numbers.Push(i) ? "ok" : "full") << std::endl;
    std::cout << "size " << numbers.Size() << " of " << numbers.Capacity() << ", Pop() = " << numbers.Pop() << ", size now " << numbers.Size() << std::endl;

    Stack<std::string, 2> words;
    words.Push("Cherno");
    words.Push("Cem");
    std::cout << "Stack<std::string, 2>: Pop() = " << words.Pop() << ", then " << words.Pop() << std::endl;
    std::cout << "sizeof(Stack<int>) = " << sizeof(Stack<int>) << ", sizeof(Stack<int, 100>) = " << sizeof(Stack<int, 100>) << std::endl;
    return 0;
}
