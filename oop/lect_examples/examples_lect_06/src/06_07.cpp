// Пример 06.06. Доминирование и множественное наследование.
#include <iostream>

using namespace std;

class A
{
public:
    void f() { cout << "Executing f from A;" << endl; }
};

class B : virtual public A
{
public:
    void f() { cout << "Executing f from B;" << endl; }
};

class C : public B, virtual public A
{
};

// треугольник это 

int main()
{
    C obj;

    obj.f();

    return 0;
}