// Пример 07.13. Особенности перегрузки оператора ->.
#include <iostream>

using namespace std;

class A
{
public:
    void f() { cout << "Executing f from A;" << endl; }
};

class B
{
private:
    A *pobj;

public:
    explicit B(A *p) : pobj(p) {}

    A *operator->()
    {
        cout << "B -> ";
        return pobj;
    }
};

class C
{
private:
    B &alias;

public:
    C(B &b) : alias(b) {}

    B &operator->()
    {
        cout << "C -> ";
        return alias;
    }
};

int main()
{
    A a;
    B b(&a);
    C c(b);

    c->f();
}