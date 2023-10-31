// Пример 09.02. Использование простого концепта.
#include <iostream>
#include <vector>

using namespace std;

template <typename T>
concept HasBeginEnd = requires(T a) {
    a.begin();
    a.end();
};

#define PRIM_1

#ifdef PRIM_1
template <typename T>
    requires HasBeginEnd<T>
ostream &operator<<(ostream &out, const T &v)
{
    for (const auto &elem : v)
        out << elem << endl;

    return out;
}

#elif defined(PRIM_2)
template <HasBeginEnd T>
ostream &operator<<(ostream &out, const T &v)
{
    for (const auto &elem : v)
        out << elem << endl;

    return out;
}

#elif defined(PRIM_3)
ostream &operator<<(ostream &out, const HasBeginEnd auto &v)
{
    for (const auto &elem : v)
        out << elem << endl;

    return out;
}

#endif

int main()
{
    vector<double> v{1., 2., 3., 4., 5.};

    cout << v;
}