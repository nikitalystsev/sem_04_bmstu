// Пример 08.18. Устранение неоднозначности зависимых имен.
#include <iostream>

template <typename T>
struct S
{
    struct Subtype
    {
    };
    template <typename U>
    void f() {}
};

template <typename T>
void g()
{
    S<T> s;
    s.template f<T>();
}

template <typename T>
void g(const T &t)
{
    //    T::Subtype* p; // Error! Идентификатор p не найден
    typename T::Subtype *p;
}

int main()
{
    g<int>();
    g(S<int>{});
}