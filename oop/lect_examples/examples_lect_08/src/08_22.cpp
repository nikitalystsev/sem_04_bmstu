// Пример 08.21. Применение бинарного оператора ко всем аргументам пакета параметров.
#include <iostream>

using namespace std;

#define Prim_3

#ifdef Prim_1
template <typename... Ts>
void ignore(Ts...)
{
}

template <typename T, typename... Ts>
auto sum(T value, Ts... params)
{
    auto result = value;
    ignore(result += params...);

    return result;
}

#elif defined(Prim_2)
template <typename... Ts>
auto sum(Ts... params)
{
    //    return (... + params);  // (..(p1 + p2) + p3) + ..)
    return (params + ...); // (p1 + (p2 + (p3 + ..)..)
}

#elif defined(Prim_3)
template <typename T, typename... Ts>
auto sum(T v1, Ts... params)
{
    cout << "call sum" << endl;
    //    return (v1 + ... + params); // (..(v1 + p1) + p2) + ..)
    return (params + ... + v1); // (v1 + (p1 + (p2 + ..)..)
}

#endif Prim_3

int main()
{
    auto s = sum(1, 2, 3, 4);

    cout << s << endl;
}