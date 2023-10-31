// Пример 06.04. Виртуальное наследование. Вызов конструкторов.
#include <iostream>

using namespace std;

class A
{
public:
    // A() { cout << "Creature A;" << endl; }
    A(const char *s) { cout << "Creature A" << s << ";" << endl; }
};

class B
{
public:
    // B() { cout << "Creature B;" << endl; }
    B(const char *s) { cout << "Creature B" << s << ";" << endl; }
};

class C : virtual public A, /*virtual*/ public B
{
public:
    C(const char *s) : A(" from C"), B(" from C") { cout << "Creature C" << s << ";" << endl; }
};

class D : virtual public A, /*virtual*/ public B
{
public:
    D(const char *s) : A(" from D"), B(" from D") { cout << "Creature D" << s << ";" << endl; }
};

class E : /*virtual*/ public C, virtual public D
{
public:
    E() : C(" from E"), D(" from E"), A(" from E") { cout << "Creature E;" << endl; }
};

int main()
{
    E obj;

    return 0;
}
