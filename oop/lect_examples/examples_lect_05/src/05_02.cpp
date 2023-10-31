// Пример 05.02. Создание и уничтожение объектов.

#include <iostream>

using namespace std;

class A
{
private:
    int value = 1;

public:
    A()
    {
        cout << "создание" << endl;
        value *= 2;
    }
    A(const A &)
    {
        cout << "копирование" << endl;
        value *= 3;
    }
    A(A &&) noexcept
    {
        cout << "перенос" << endl;
        value *= 4;
    }
    ~A() { cout << value << endl; }
};

A f(A obj)
{
    cout << "функция f" << endl;
    return obj;
}

A f1()
{
    cout << "функция f1" << endl;
    return A();
}

A f2()
{
    A obj;

    cout << "функция f2" << endl;

    return obj;
}

int main()
{
    cout << "prim 1" << endl;
    {
        A obj;

        f(obj);
    }
    cout << "prim 2" << endl;
    {
        A obj = f1();
    }
    cout << "prim 3" << endl;
    {
        A obj = f2();
    }
}
