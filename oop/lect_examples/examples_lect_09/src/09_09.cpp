// Пример 09.09. Ограничения для шаблонов классов, использование дизъюнкции.
#include <iostream>

using namespace std;

template <typename T>
concept Ord = requires(T t1, T t2) { t1 < t2; };

template <typename T>
concept Void = is_same_v<T, void>;

template <typename T = void>
    requires Ord<T> || Void<T>
struct Less;

template <Ord T>
struct Less<T>
{
    bool operator()(T a, T b) const
    {
        cout << "первый метод" << endl;
        return a < b;
    }
};

template <>
struct Less<void>
{
    template <Ord T>
    bool operator()(T &a, T &b) const
    {
        cout << "второй метод" << endl;
        return &a < &b;
    }
};

int main()
{
    Less<double> d1;

    cout << boolalpha << d1(2., 3.) << endl;

    Less d2;

    int a = 0, b = 1;
    cout << boolalpha << d2(a, b) << endl;
}