// Пример 08.26. Использование вариативных выражений для потоков вывода.
#include <iostream>

using namespace std;

template <typename T>
class AddSpace
{
private:
    const T &ref;

public:
    AddSpace(const T &r) : ref(r) {}

    friend ostream &operator<<(ostream &os, AddSpace as)
    {
        return os << ' ' << as.ref;
    }
};

template <typename... Ts>
ostream &print(ostream &os, Ts &&...args)
{
    return (os << ... << AddSpace(forward<Ts>(args)));
}

int main()
{
    print(cout, 1, 2, 3, 4, 5) << endl;
}