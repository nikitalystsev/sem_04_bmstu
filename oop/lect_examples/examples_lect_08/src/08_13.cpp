// Пример 08.12. Свертка ссылок и вывод типа параметра шаблонного метода класса.
#include <iostream>

template <typename T>
class A
{
public:
    T f(T &&t) { return t; }
    template <typename U>
    T g(U &&u) { return u; }
};

int main()
{
    A<int> obj{};
    int i;

    // obj.f(i);// Error!
    obj.g(i); // int A<int>::g<int&>(int&)

    obj.f(0); // int A<int>::f(int&&)
    obj.g(0); // int A<int>::g<int>(int&&)
}