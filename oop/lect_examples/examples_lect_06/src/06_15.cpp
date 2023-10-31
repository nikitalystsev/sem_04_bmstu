// Пример 06.14. Чисто виртуальный деструктор.

#include <iostream>

using namespace std;

class A
{
public:
    virtual ~A() = 0;
};

A::~A() = default;

class B : public A
{
public:
    ~B() override { cout << "Class B destructor called;" << endl; }
};

int main()
{
    A *pobj = new B;

    delete pobj;

    return 0;
}