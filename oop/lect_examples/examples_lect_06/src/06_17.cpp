// Пример 06.16. Выведение типа возвращаемого значения методом.

#include <iostream>

using namespace std;

class Base
{
public:
    ~Base() = default;

    virtual const int &f() const & = 0;
    virtual int f() && = 0;
};

class Derived final : public Base
{
public:
    auto f() const & -> const int & final
    {
        cout << "Derived::f() const&" << endl;
        return 0;
    }
    auto f() && -> int override
    {
        cout << "Derived::f()&&" << endl;
        return 0;
    }
    auto g() const
    {
        cout << "Derived::g() const" << endl;
        return 0;
    }
    auto g()
    {
        cout << "Derived::g()" << endl;
        return 0.;
    }
};

int main()
{
    const Derived child1{};
    Derived child2;

    Base &obj = child2;

    decltype(auto) d1 = obj.f();
    decltype(auto) d2 = move(obj).f();
    auto d3 = child1.g();
    auto d4 = child2.g();

    return 0;
}