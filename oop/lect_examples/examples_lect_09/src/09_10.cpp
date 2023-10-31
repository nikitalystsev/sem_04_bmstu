// Пример 09.18. Использование концептов на примере класс Array.
#include <iostream>
#include <initializer_list>
#include <vector>

using namespace std;

template <typename From, typename To>
concept Convertable = convertible_to<From, To>;

template <typename From, typename To>
concept Assignable = requires(From fm, To to) {
    to = fm;
};

template <typename Type>
concept Container = requires(Type t) {
    typename Type::value_type;
    typename Type::size_type;
    typename Type::iterator;
    typename Type::const_iterator;

    {
        t.size()
    } noexcept -> same_as<typename Type::size_type>;
    {
        t.end()
    } noexcept -> same_as<typename Type::iterator>;
    {
        t.begin()
    } noexcept -> same_as<typename Type::iterator>;
};

template <typename T>
class Array
{
public:
    using value_type = T;
    using size_type = size_t;

private:
    value_type *arr{nullptr};
    size_t count{0};

public:
    Array(initializer_list<T> lt);
    explicit Array(const Array &ar);
    Array(Array &&ar) noexcept;
    template <Convertable<T> U> // Convertable<U, T>
    Array(const Array<U> &other);
    template <Container Con>
        requires Convertable<typename Con::value_type, T> && Assignable<typename Con::value_type, T>
    Array(const Con &other);
    ~Array();

    size_t size() const noexcept { return count; }

    T &operator[](int index) { return arr[index]; }
    const T &operator[](int index) const { return arr[index]; }
};

template <typename T>
Array<T>::Array(initializer_list<T> lt) : count(lt.size())
{
    if (!count)
        return;

    arr = new T[count];

    for (int i = 0; auto elem : lt)
        arr[i++] = elem;
}

template <typename T>
Array<T>::Array(const Array &ar) : count(ar.count)
{
    if (!count)
        return;

    arr = new T[count];

    for (int i = 0; i < count; i++)
        arr[i] = ar.arr[i];
}

template <typename T>
Array<T>::Array(Array &&ar) noexcept : count(ar.count), arr(ar.arr)
{
    ar.arr = nullptr;
}

template <typename T>
template <Convertable<T> U>
Array<T>::Array(const Array<U> &other) : count(other.size())
{
    if (!count)
        return;

    arr = new T[count];

    for (int i = 0; i < count; i++)
        arr[i] = other[i];
}

template <typename T>
template <Container Con>
    requires Convertable<typename Con::value_type, T> && Assignable<typename Con::value_type, T>
Array<T>::Array(const Con &other) : count(other.size())
{
    if (!count)
        return;

    arr = new T[count];

    for (size_t i = 0; auto elem : other)
        arr[i++] = elem;
}

template <typename T>
Array<T>::~Array()
{
    delete[] arr;
}

int main()
{
    Array a1{1, 2, 3};
    Array a2{1., 2., 3.};
    Array<int> a3{move(a1)};
    Array<int> a4(move(a2));

    vector v{1., 3., 5.};
    Array<int> a5(v);
}
