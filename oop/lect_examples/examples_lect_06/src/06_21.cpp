// Пример 06.20. Дружба и наследование.
#include <iostream>

using namespace std;

class C; // forward объявление

class A
{
private:
    void f1() { cout << "Executing f1;" << endl; }

    friend C;
};

class B : public A
{
private:
    void f2() { cout << "Executing f2;" << endl; }
};

class C
{
public:
    static void g1(A &obj) { obj.f1(); }
    static void g2(B &obj)
    {
        obj.f1();
        // obj.f2(); // Error!!! Имеет доступ только к членам A
    }
};

class D : public C
{
public:
    // static void g2(A& obj) ( obj.f1(); } // Error!!! Дружба не наследуется
};

int main()
{
    A aobj;

    C::g1(aobj);

    B bobj;

    C::g1(bobj);
    C::g2(bobj);

    return 0;
}
