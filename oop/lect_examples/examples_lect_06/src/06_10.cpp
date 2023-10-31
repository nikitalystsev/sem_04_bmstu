// Пример 06.09. Неоднозначности при множественном наследовании.

#include <iostream>

class A
{
public:
    int a;
    int (*b)();
    int f();
    int f(int);
    int g();
};

class B
{
    int a;
    int b;

public:
    int f();
    int g;
    int h();
    int h(int);
};

class C : public A, public B
{
};

class D
{
public:
    static void fun(C &obj)
    {
        // obj.a = 1; // Error!!!
        // obj.b();   // Error!!!
        // obj.f();   // Error!!!
        // obj.f(1);  // Error!!!
        // obj.g = 1; // Error!!!
        // obj.h();
        // obj.h(1); // Ok!
    }
};

int main()
{
    C obj;

    D::fun(obj);

    return 0;
}