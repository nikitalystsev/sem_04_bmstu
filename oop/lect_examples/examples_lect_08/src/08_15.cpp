// Пример 08.14. Использование forward для идеальной передачи (lvalue-copy, rvalue-move).
#include <iostream>

using namespace std;

class A
{
public:
    A() = default;
    A(const A &) { cout << "Copy constructor" << endl; }
    A(A &&) noexcept { cout << "Move constructor" << endl; }
};

template <typename Func, typename Arg>
decltype(auto) call(Func &&func, Arg &&arg)
{
    //    return func(arg);
    cout << "call call" << endl;
    return forward<Func>(func)(forward<Arg>(arg));
}

A f(A a)
{
    cout << "f called" << endl;
    return a;
}

int main()
{
    A obj{};

    auto r1 = call(f, obj);
    cout << endl;
    auto r2 = call(f, move(obj));
}