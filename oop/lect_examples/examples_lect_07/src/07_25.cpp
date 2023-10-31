// Пример 07.25. Определение литеральных операторов.
#include <iostream>
#include <assert.h>
#include <cstring>

using namespace std;

unsigned long long operator"" _b(const char *str)
{
    size_t size = strlen(str);

    unsigned long long result = 0;
    for (size_t i = 0; i < size; ++i)
    {
        assert(str[i] == '1' || str[i] == '0');
        (result <<= 1) |= str[i] - '0';
    }

    return result;
}

double operator"" _kg(long double val)
{
    return val;
}

int main()
{
    cout << 101100_b << endl;
    cout << 76.3_kg << endl;
}