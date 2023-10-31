// Пример 08.06. Специализация шаблона функции.
#include <iostream>

using namespace std;

template <typename T>
T get_value();

template <>
int get_value() { return 413; }

template <>
double get_value() { return 3.14; }

int main()
{
    auto x = get_value<int>();
    auto y = get_value<double>();
    // auto z = get_value<float>(); // Error linker!

    cout << " x= " << x << " y = " << y << endl;
}
