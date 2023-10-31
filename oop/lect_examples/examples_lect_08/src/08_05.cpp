// Пример 08.04. Свертка ссылок и вывод типа шаблонного параметра.
#include <iostream>

using namespace std;

template <typename T>
T f(T &&x) { return x; }

int main()
{
    int a;
    const int b = 0;

    f(a); // int& f<int&>(int&)
    f(b); // const int& f<const int&>(const int&)
    f(0); // int f<int>(int&&)
}