// Пример 09.01. Выбор шаблона(специализации)
// подстановкой параметров(инстанцирование).
#include <iostream>

using namespace std;

#define PRIM_5

#ifdef PRIM_1
template <typename T, bool>
struct PrintHelper
{
    static void print(const T &t) { cout << t << endl; }
};

template <typename T>
struct PrintHelper<T, true>
{
    static void print(const T &t) { cout << *t << endl; }
};

template <typename T>
void print(const T &t)
{
    PrintHelper<T, is_pointer_v<T>>::print(t);
}

#elif defined(PRIM_2)
template <typename T>
void printHelper(false_type, const T &t)
{
    cout << t << endl;
}

template <typename T>
void printHelper(true_type, const T &t) { cout << *t << endl; }

template <typename T>
void print(const T &t)
{
    printHelper(typename is_pointer<T>::type{}, t);
}

#elif defined(PRIM_3)
template <typename T>
void print(const T &t)
{
    if constexpr (is_pointer_v<T>)
    {
        cout << *t << endl;
    }
    else
    {
        cout << t << endl;
    }
}

#elif defined(PRIM_4)
void print(auto &t)
{
    cout << t << endl;
}

void print(auto *t)
{
    cout << *t << endl;
}

#elif defined(PRIM_5)
void print(const auto &t)
{
    cout << "пример 5" << endl;
    cout << t << endl;
}

template <typename T>
concept pointer = is_pointer_v<T>;

void print(const pointer auto &t)
{
    cout << "с концептом" << endl;
    cout << *t << endl;
}

#endif

int main()
{
    double d = 1.5;

    print(d);
    print(&d);
}
