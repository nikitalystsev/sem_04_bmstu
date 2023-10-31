// Пример 08.11. Шаблонный метод шаблонного класса.
#include <iostream>

using namespace std;

template <typename T>
class A
{
private:
    T elem;

public:
    A(const T &d) : elem(d) {}

    template <typename U>
    auto sum(U d); // -> decltype(d + this->A<T>::elem);
};

template <typename T>
template <typename U>
auto A<T>::sum(U d) // -> decltype(d + this->A<T>::elem)
{
    return elem + d;
}

int main()
{
    A obj(1);

    cout << obj.sum(1.1) << endl;
}