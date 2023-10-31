// Пример 06.07. Множественный вызов методов.
#include <iostream>

using namespace std;

class A
{
public:
    void f() { cout << "Executing f from A;" << endl; }
};

class B : virtual public A
{
public:
    void f()
    {
        A::f();
        cout << "Executing f from B;" << endl;
    }
};

class C : virtual public A
{
public:
    void f()
    {
        A::f();
        cout << "Executing f from C;" << endl;
    }
};

class D : virtual public C, virtual public B
{
public:
    void f()
    {
        C::f();
        B::f();
        cout << "Executing f from D;" << endl;
    }
};

int main()
{
    D obj;

    obj.f();

    return 0;
}