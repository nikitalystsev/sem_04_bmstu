// Пример 08.24. Шаблон класса с переменным числом параметров значений.
#include <iostream>

using namespace std;

template <size_t...>
struct Sum
{
};

template <>
struct Sum<>
{
    enum
    {
        value = 0
    };
};

template <size_t val, size_t... args>
struct Sum<val, args...>
{
    enum
    {
        value = val + Sum<args...>::value
    };
};

int main()
{
    cout << Sum<1, 2, 3, 4>::value << endl;
}
