// Пример 06.18. Проблема передачи объектов в метод по значению.
#include <iostream>

using namespace std;

class A
{
public:
    virtual ~A() = default;
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
    static void g(A obj) { obj.f(); }
};

int main()
{
    const A &obj = B{};

    C::g(obj);

    return 0;
}
