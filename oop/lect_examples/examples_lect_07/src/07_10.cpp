// Пример 07.10. Использование оператора ->*.
#include <iostream>

using namespace std;

class Callee;

class Caller
{
    using FnPtr = int (Callee::*)(int);  // указатель на метод класса Callee

private:
    Callee *pobj;
    FnPtr ptr;

public:
    Caller(Callee *p, FnPtr pf) : pobj(p), ptr(pf) {}

    int call(int d) { return (pobj->*ptr)(d); }
};

class Callee
{
private:
    int index;

public:
    Callee(int i = 0) : index(i) {}

    int inc(int d) { return index += d; }
    int dec(int d) { return index -= d; }
};

int main()
{
    Callee obj;
    Caller cl1(&obj, &Callee::inc);
    Caller cl2(&obj, &Callee::dec);

    cout << " 1: " << cl1.call(3) << "; 2: " << cl2.call(5) << endl;
}