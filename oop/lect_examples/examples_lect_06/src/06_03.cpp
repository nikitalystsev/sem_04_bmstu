// Пример 06.03. Виртуальное наследование.
#include <iostream>

using namespace std;

class A
{
public:
    A(const char *s) { cout << "Creature A" << s << ";" << endl; }
};

class B : virtual public A
{
public:
    B() : A(" from B") { cout << "Creature B;" << endl; }
};

class C : public B, virtual public A
{
public:
    C() : A(" from C") { cout << "Creature C;" << endl; }
};

int main()
{
    C obj;

    return 0;
}
