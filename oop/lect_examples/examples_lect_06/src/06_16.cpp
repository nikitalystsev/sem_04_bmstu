// Пример 06.15. Вызов виртуальных методов в конструкторах и деструкторах.
#include <iostream>

using namespace std;

class A
{
public:
    virtual ~A() { cout << "Class A destructor called;" << endl; }

    virtual void f() { cout << "Executing f from A;" << endl; }
};

class B : public A
{
public:
    B() { this->f(); }
    ~B() override
    {
        this->f();
        cout << "Class B destructor called;" << endl;
    }

    void g() { this->f(); }
};

class C : public B
{
public:
    ~C() override { cout << "Class C destructor called;" << endl; }

    void f() override { cout << "Executing f from C;" << endl; }
};

int main()
{
    C obj;

    obj.g();

    return 0;
}
