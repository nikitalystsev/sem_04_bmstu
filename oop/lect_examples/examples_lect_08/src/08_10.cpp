// Пример 08.09. Конструкторы для вывода типа параметра шаблона класса.
#include <iostream>
#include <initializer_list>
#include <vector>

using namespace std;

template <typename Type>
class Array
{
private:
    Type *arr;
    size_t count;

public:
    Array(initializer_list<Type> lst) : count(lst.size())
    {
        arr = new Type[count]{};

        for (size_t i = 0; auto &&elem : lst)
            arr[i++] = elem;
    }
    template <typename Iter>
    Array(Iter ib, Iter ie) : count(ie - ib)
    {
        arr = new Type[count]{};

        size_t i = 0;
        for (auto it = ib; it != ie; ++it, i++)
            arr[i] = *it;
    }

    template <typename U>
    friend ostream &operator<<(ostream &os, const Array<U> &ar);
};

// Вывод параметра шаблона класса Array
template <typename Iter>
Array(Iter ib, Iter ie) -> Array<typename iterator_traits<Iter>::value_type>;

template <typename U>
ostream &operator<<(ostream &os, const Array<U> &ar)
{
    if (!ar.count)
        return os;

    os << ar.arr[0];
    for (size_t i = 1; i < ar.count; ++i)
        os << ", " << ar.arr[i];

    return os;
}

int main()
{
    Array a1{1., 2., 3.};

    cout << a1 << endl;

    vector v{4., 5., 6.};
    auto a2 = Array(v.begin(), v.end());

    cout << a2 << endl;
}
