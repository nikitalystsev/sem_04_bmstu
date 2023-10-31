// Пример 06.19. Множественное наследование и виртуальные методы.
#include <iostream>

using namespace std;

class A
{
public:
    virtual ~A() = 0;

    virtual void f() { cout << "Executing f from A;" << endl; }
};

A::~A() {}

class B
{
public:
    virtual ~B() = 0;

    virtual void f() { cout << "Executing f from B;" << endl; }
};

B::~B() {}

class C : private A, public B
{
public:
    ~C() override {}

    void f() override { cout << "Executing f from C;" << endl; }
};

class D
{
public:
    void g1(A &obj)
    {
        obj.f();
    }
    void g2(B &obj)
    {
        obj.f();
    }
};

int main()
{
    C obj;
    D d;

    d.g2(obj);
    d.g2(obj);

    return 0;
}