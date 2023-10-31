// Пример 06.12. Виртуальные методы.

#include <iostream>

using namespace std;

class A
{
public:
    virtual void f() { cout << "Executing f from A;" << endl; }
};

class B : public A
{
public:
    void f() override { cout << "Executing f from B;" << endl; }
};

class C
{
public:
    static void g(A &obj) { obj.f(); }
};

int main()
{
    B obj;

    C::g(obj);

    return 0;
}