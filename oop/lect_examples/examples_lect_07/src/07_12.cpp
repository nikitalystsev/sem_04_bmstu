// Пример 07.12. “Умные” указатели. Перегрузка операторов -> и *.
#include <iostream>

using namespace std;

class A
{
public:
    void f() const { cout << "Executing f from A;" << endl; }
};

class B
{
private:
    A *pobj;

public:
    B(A *p) : pobj(p) {}

    A *operator->() noexcept { return pobj; }
    const A *operator->() const noexcept { return pobj; }
    A &operator*() noexcept { return *pobj; }
    const A &operator*() const noexcept { return *pobj; }
};

int main()
{
    A a;

    B b1(&a);
    b1->f();

    const B b2(&a);
    (*b2).f();
}