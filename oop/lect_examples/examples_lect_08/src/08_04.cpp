// Пример 08.03. “Срезание” ссылок и константности при выводе типа шаблона.
#include <iostream>

using namespace std;

#define PRIM_05

#ifdef PRIM_01
template <typename T>
T sum(T x, T y)
{
    return x + y;
}

#elif defined(PRIM_02)
template <typename T>
T sum(T &x, T &y)
{
    return x + y;
}

#elif defined(PRIM_03)
auto sum(auto x, auto y)
{
    return x + y;
}

#elif defined(PRIM_04)
auto sum(auto &x, auto &y)
{
    return x + y;
}

#elif defined(PRIM_05)
auto sum(auto &&x, auto &&y)
{
    return x + y;
}

#endif

int main()
{
    const int &a = 1, &b = 2;

    cout << sum(a, b) << endl;
    // 1) T(T, T) -> int sum<int>(int, int)
    // 2) T(T&, T&) -> const int sum<const int>(const int&, const int&)
    // 3) auto(auto, auto) -> int sum<int, int>(int, int)
    // 4) auto(auto&, auto&) -> const int sum<const int, const int>(const int&, const int&)
    // 5) auto(auto&&, auto&&) -> const int sum<const int&, const int&>(const int&, const int&)

    int c = 3, &d = c;

    cout << sum(c, d) << endl;
    // 1) T(T, T) -> int sum<int>(int, int)
    // 2) T(T&, T&) -> int sum<int>(int&, int&)
    // 3) auto(auto, auto) -> int sum<int, int>(int, int)
    // 4) auto(auto&, auto&) -> int sum<int, int>(int&, int&)
    // 5) auto(auto&&, auto&&) -> int sum<int&, int&>(int&, int&)
}