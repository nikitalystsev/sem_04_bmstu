// Пример 07.14. Использование виртуальных операторов -> и *. Ковариантность.
#include <iostream>

using namespace std;

class A
{
public:
    void g() { cout << "A::g" << endl; }
};

class B : public A
{
public:
    void g() { cout << "B::g" << endl; }
};

class Base
{
public:
    virtual ~Base() = default;

    virtual A *operator->() = 0;
    virtual A &operator*() = 0;
};

class C : public Base
{
private:
    A *ptr = new A;

public:
    ~C() override { delete ptr; }

    A *operator->() override { return ptr; }
    A &operator*() override { return *ptr; }
};

class D : public Base
{
private:
    B *ptr = new B;

public:
    ~D() override { delete ptr; }

    B *operator->() override { return ptr; }
    B &operator*() override { return *ptr; }
};

int main()
{
    D obj;
    obj->g();
    (*obj).g();

    Base &alias = obj;
    alias->g();
    (*alias).g();
}
