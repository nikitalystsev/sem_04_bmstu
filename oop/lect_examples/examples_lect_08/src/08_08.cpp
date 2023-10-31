// Пример 08.07. Шаблон класса, шаблоны методов (без обработки исключительных ситуаций).
#include <iostream>

using namespace std;

template <typename Type, size_t N>
class Array
{
private:
    Type arr[N];

public:
    Array() = default;
    Array(initializer_list<Type> lt);

    Type &operator[](int ind);
    const Type &operator[](int ind) const;

    bool operator==(const Array &a) const;

    template <typename Type, size_t N>
    friend Array<Type, N> operator+(const Array<Type, N> &a1, const Array<Type, N> &a2);
};

template <typename Type, size_t N>
Array<Type, N>::Array(initializer_list<Type> lt)
{
    int n = N <= lt.size() ? N : lt.size();
    auto it = lt.begin();
    int i;
    for (i = 0; i < n; i++, ++it)
        arr[i] = *it;

    for (; i < N; i++)
        arr[i] = 0.;
}

template <typename Type, size_t N>
Type &Array<Type, N>::operator[](int ind) { return arr[ind]; }

template <typename Type, size_t N>
const Type &Array<Type, N>::operator[](int ind) const { return arr[ind]; }

template <typename Type, size_t N>
bool Array<Type, N>::operator==(const Array &a) const
{
    if (this == &a)
        return true;

    bool Key = true;
    for (int i = 0; Key && i < N; i++)
        Key = arr[i] == a.arr[i];

    return Key;
}

template <typename Type, size_t N>
Array<Type, N> operator+(const Array<Type, N> &a1, const Array<Type, N> &a2)
{
    Array<Type, N> res;

    for (int i = 0; i < N; i++)
        res.arr[i] = a1.arr[i] + a2.arr[i];

    return res;
}

template <typename Type, size_t N>
ostream &operator<<(ostream &os, const Array<Type, N> &a)
{
    for (int i = 0; i < N; i++)
        os << a[i] << " ";

    return os;
}

int main()
{
    Array<double, 3> a1{1, 2, 3}, a2{1, 2, 3}, a3{4, 2};

    if (a1 == a2)
        a1 = a2 + a3;

    cout << a1 << endl;
}