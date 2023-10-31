// Пример 10.10. Приведение типов в С++. Использование static_cast и dynamic_cast.
#include <iostream>

using namespace std;

class A
{
    int a = 0;

public:
    virtual ~A() = 0;

    void f() { cout << "method f class A:" << a << endl; }
};

A::~A() {}

class B : public A
{
    int b = 1;

public:
    void f() { cout << "method f class B;" << b << endl; }

    void g1() { cout << "method g1 class B;" << endl; }
};

class C : public B
{
    int c = 2;

public:
    void f() { cout << "method f class C;" << c << endl; }

    void g2() { cout << "method g2 class B;" << endl; }
};

class D : public A
{
    int d = 3;

public:
    void f() { cout << "method f class D;" << d << endl; }
};

int main()
{
    A *pa = new B;

    B *pb = static_cast<B *>(pa);

    pb->f();

    C *pc = static_cast<C *>(pa);

    pc->f();

    D *pd = static_cast<D *>(pa);

    pd->f();

    pb = dynamic_cast<B *>(pa);
    if (!pb)
    {
        cout << "Error bad cast!" << endl;
    }
    else
    {
        pb->f();
        pb->g1();
    }

    pc = dynamic_cast<C *>(pa);
    if (!pc)
    {
        cout << "Error bad cast!" << endl;
    }
    else
    {
        pc->f();
        pc->g2();
    }

    const B obj;
    const B *p = &obj;

    const_cast<B *>(p)->f();
}