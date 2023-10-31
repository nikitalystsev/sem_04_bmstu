
// Пример 07.15. Перегрузка оператора ->*. Функтор.
#include <iostream>

using namespace std;

class Callee
{
private:
    int index;

public:
    Callee(int i = 0) : index(i) {}

    int inc(int d) { return index += d; }
};

class Caller
{
public:
    using FnPtr = int (Callee::*)(int); // указатель на метод класса Callee

private:
    Callee *pobj;
    FnPtr ptr;

public:
    Caller(Callee *p, FnPtr pf) : pobj(p), ptr(pf) {}

    int operator()(int d) { return (pobj->*ptr)(d); }
};

class Pointer
{
private:
    Callee *pce;

public:
    Pointer(int i) { pce = new Callee(i); }
    ~Pointer() { delete pce; }

    Caller operator->*(Caller::FnPtr pf) { return Caller(pce, pf); }
};

int main()
{
    Caller::FnPtr pn = &Callee::inc;

    Pointer pt(1);

    cout << "Result: " << (pt->*pn)(2) << endl;
}
