// Пример 08.10. Шаблонный метод класса.
#include <iostream>

using namespace std;

class A
{
public:
    template <typename Type>
    const Type &f(const Type &elem);
};

template <typename Type>
const Type &A::f(const Type &elem) { return elem; }

int main()
{
    A obj;

    cout << obj.f(2.) << endl;
    cout << obj.f("String") << endl;
}
