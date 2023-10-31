// Пример 08.16. Полная специализация шаблона класса и метода шаблона класса.
#include <iostream>

using namespace std;

template <typename Type>
class A
{
public:
    A() { cout << "constructor of template A;" << endl; }
    void f() { cout << "metod f of template A;" << endl; }
};

template <>
void A<int>::f() { cout << "specialization of metod f of template A;" << endl; }

template <>
class A<float>
{
public:
    A() { cout << "specialization constructor template A;" << endl; }
    void f() { cout << "metod f specialization template A;" << endl; }
    void g() { cout << "metod g specialization template A;" << endl; }
};

int main()
{
    A<double> obj1;
    obj1.f();

    A<float> obj2;
    obj2.f();
    obj2.g();

    A<int> obj3;
    obj3.f();
}