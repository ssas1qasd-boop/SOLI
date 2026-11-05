#include <iostream>
#include <cstring>

class String
{
private:
    char* m_Buffer;
    unsigned int m_Size;

public:
    String(const char* string)
    {
        m_Size = strlen(string);
        m_Buffer = new char[m_Size + 1];
        memcpy(m_Buffer, string, m_Size);
        m_Buffer[m_Size] = 0;
    }

    String(const String& other)
        : m_Size(other.m_Size)
    {
        std::cout << "Copied!" << std::endl;
        m_Buffer = new char[m_Size + 1];
        memcpy(m_Buffer, other.m_Buffer, m_Size + 1);
    }

    ~String()
    {
        delete[] m_Buffer;
    }

    char& operator[](unsigned int index)
    {
        return m_Buffer[index];
    }

    const void* Data() const
    {
        return m_Buffer;
    }

    friend std::ostream& operator<<(std::ostream& stream, const String& string);
};

std::ostream& operator<<(std::ostream& stream, const String& string)
{
    stream << string.m_Buffer;
    return stream;
}

void PrintByValue(String string)
{
    std::cout << "by value: " << string << std::endl;
}

void PrintByReference(const String& string)
{
    std::cout << "by const reference: " << string << std::endl;
}

int main()
{
    String string = "Cherno";
    String second = string;
    second[2] = 'a';
    std::cout << string << " / " << second << std::endl;
    std::cout << "buffers: " << string.Data() << " and " << second.Data() << std::endl;

    PrintByValue(string);
    PrintByValue(second);
    PrintByReference(string);
    PrintByReference(second);
    return 0;
}
