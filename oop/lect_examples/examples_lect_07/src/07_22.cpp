// Пример 07.22. Оператор приведения типа с автоматическим выведением типа.
#include <iostream>

class A
{
private:
    int val;

public:
    A(int i) : val(i) {}

    operator auto() const & { return val; }
    operator auto() && { return val; }
    operator auto *() const { return &val; }
};

int main()
{
    A obj{10};

    int v1 = obj;            // operator auto() const&
    double v2 = obj;         // operator auto() const&
    const double &al = obj;  // operator auto() const&
    int v3 = std::move(obj); // operator auto()&&
    const int *p = obj;      // operator auto*() const
}
