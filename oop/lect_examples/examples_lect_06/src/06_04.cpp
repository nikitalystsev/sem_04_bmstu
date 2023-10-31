// Пример 06.041. Виртуальное наследование (проблема).
#include <iostream>

using namespace std;

class A
{
public:
    A() { cout << "Creature A;" << endl; }
    A(const char *s) { cout << "Creature A" << s << ";" << endl; }
};

class B : virtual public A
{
public:
    B(const char *s) : A() { cout << "Creature B" << s << ";" << endl; }
};

class C : /*virtual*/ public A
{
public:
    C(const char *s) : A() { cout << "Creature C" << s << ";" << endl; }
};

class D : public B, public C
{
public:
    D() : B(" from D"), C(" from D") { cout << "Creature D;" << endl; }
};

int main()
{
    D obj;

    return 0;
}
