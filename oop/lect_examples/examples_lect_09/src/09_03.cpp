// Пример 09.03. Варианты использования концепта.
#include <iostream>

using namespace std;

template <typename T>
concept Incrementable = requires(T t) {
    {
        ++t
    } noexcept;
    t++;
};

#define PRIM_1

#ifdef PRIM_1
template <typename T>
    requires Incrementable<T>
auto inc(T &arg)
{
    return ++arg;
}

#elif defined(PRIM_2)
template <typename T>
auto inc(T &arg)
    requires Incrementable<T>
{
    return ++arg;
}

#elif defined(PRIM_3)
template <Incrementable T>
auto inc(T &arg)
{
    return ++arg;
}

#elif defined(PRIM_4)
auto inc(Incrementable auto &arg)
{
    return ++arg;
}

#elif defined(PRIM_5)
template <typename T>
    requires requires(T t) {
        {
            ++t
        } noexcept;
        {
            t++
        };
    }
auto inc(T &arg)
{
    return ++arg;
}

#endif

class A
{
};

int main()
{
    int i = 0;

    cout << "i = " << inc(i) << endl;

    A obj{};

    //    cout << "obj = " << inc(obj) << endl;
}