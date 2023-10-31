// Пример 09.11. Применение unique_ptr.
#include <iostream>
#include <memory>

using namespace std;

class A
{
public:
    A() { cout << "Constructor" << endl; }
    ~A() { cout << "Destructor" << endl; }

    void f() { cout << "Function f" << endl; }
};

int main()
{
    unique_ptr<A> obj1(new A{});
    unique_ptr<A> obj2 = make_unique<A>();
    unique_ptr<A> obj3(obj1.release()); // move(obj1)

    obj1 = move(obj3);

    if (!obj3)
    {
        A *p = obj1.release();

        obj2.reset(p);
        obj2->f();
    }
}