// Пример 08.28. Использование указателя this.
#include <iostream>

using namespace std;

template <typename Т>
class Base
{
public:
    void f() { cout << "method f is called" << endl; }
};

template <typename T>
class Derived : public Base<T>
{
public:
    void func()
    {
            //    f();    // идентификатор f не найден
        this->f();
    }
};

int main()
{
    Derived<int> obj{};

    obj.func();
}
