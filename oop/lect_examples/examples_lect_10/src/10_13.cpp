// Пример 10.13. Использование reinterpret_cast.
#include <iostream>
#include <string.h>

using namespace std;

class A
{
private:
    int a{63};
    char s[6];

public:
    A(const char *st) { strcpy_s(s, st); }
};

void print(const char *st, size_t len)
{
    for (size_t i = 0; i < len; i++)
        cout << st[i];
}

int main()
{
    A obj("Ok!!!");
    char *pByte = reinterpret_cast<char *>(&obj);

    print(pByte, sizeof(obj));
}