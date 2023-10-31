// Пример 06.11. Объединение интерфейсов.
#include <iostream>

using namespace std;

class A
{
public:
    void f1() { cout << "Executing f1 from A;" << endl; }
    void f2() { cout << "Executing f2 from A;" << endl; }
};

class B
{
public:
    void f1() { cout << "Executing f1 from B;" << endl; }
    void f3() { cout << "Executing f3 from B;" << endl; }
};

class C : public A, public B
{
};

class D
{
public:
    void g1(A &obj)
    {
        obj.f1();
        obj.f2();
    }
    void g2(B &obj)
    {
        obj.f1();
        obj.f3();
    }
};

int main()
{
    C obj;

    D d;

    d.g1(obj);
    d.g2(obj);

    return 0;
}