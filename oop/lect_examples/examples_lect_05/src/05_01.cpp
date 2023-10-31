// Пример 05.01. Вызов методов по lvalue и rvalue ссылкам.

#include <iostream>

using namespace std;

class A
{
private:
    int a;
    mutable int b;

public:
    // A() : a(1), b(1) {}
    // A(const A &a) { cout << "конструктор копирования" << endl; }
    // A(A &&a) { cout << "конструктор переноса" << endl; }
    int f() &
    {
        cout << "int()&" << endl;
        return ++a;
    }
    int f() const &
    {
        cout << "int() const&" << endl;
        //        ++a; // Error!

        return ++b;
    }
    int f() &&
    {
        cout << "int()&&" << endl;
        return b += a;
    }
    //  int f() {} // Error!
};

A func(const A &obj)
{
    cout << "вызов функции func" << endl;
    return obj;
}

int main()
{
    A obj1;
    const A obj2{};

    obj1.f();
    obj2.f();
    move(obj1).f();

    A().f();
    func(obj1).f();
}