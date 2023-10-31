// Пример 06.08. Решение проблемы множественного вызова методов.
#include <iostream>

using namespace std;

class A
{
protected:
    void _f() { cout << "Executing f from A;" << endl; }

public:
    void f() { this->_f(); }
};

class B : virtual public A
{
protected:
    void _f() { cout << "Executing f from B;" << endl; }

public:
    void f()
    {
        A::_f();
        this->_f();
    }
};

class C : virtual public A
{
protected:
    void _f() { cout << "Executing f from C;" << endl; }

public:
    void f()
    {
        A::_f();
        this->_f();
    }
};

class D : virtual public C, virtual public B
{
protected:
    void _f() { cout << "Executing f from D;" << endl; }

public:
    void f()
    {
        A::_f();
        C::_f();
        B::_f();
        this->_f();
    }
};

int main()
{
    D obj;

    obj.f();

    return 0;
}
