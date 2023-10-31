//  Пример 10.11. dynamic_cast – приведение между базовыми классами.
#include <iostream>

using namespace std;

class Base
{
public:
    virtual ~Base() = default;

    virtual void f() = 0;
};

class A : public Base
{
public:
    void f() override { cout << "function f (class A)" << endl; }
};

class B
{
public:
    virtual ~B() = default;

    virtual void g() = 0;
};

class C : public A, public B
{
public:
    void f() override { cout << "function f (class C)" << endl; }
    void g() override { cout << "function g" << endl; }
};

int main()
{
    A *pa = new C;
    pa->f();
    // pa->g(); // Error!

    B *pb1 = dynamic_cast<B *>(pa);
    // pb1->f(); // Error!
    pb1->g();

    Base *p = dynamic_cast<Base *>(pb1);
    p->f();

    B *pb2 = dynamic_cast<B *>(p);
    pb2->g();

    delete pa;
}
