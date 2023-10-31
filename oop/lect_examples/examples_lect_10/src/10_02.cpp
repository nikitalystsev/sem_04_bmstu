// Пример 10.02. Использование оператора -> для итераторов.
#include <iostream>
#include <vector>
#include <iterator>

using namespace std;

class A
{
private:
    int a;
    static int q;

public:
    A() { a = ++q; }

    void f() { cout << a << endl; }
};

int A::q = 0;

int main()
{
    vector<A> vec(10);

    for (auto it = vec.begin(); it != vec.end(); ++it)
        it->f();
}