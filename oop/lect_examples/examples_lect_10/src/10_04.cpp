// Пример 10.04. Пример: числа Фибоначчи.
#include <iostream>

using namespace std;

struct fibonacci
{
    int num{0};
};

class Fibiter
{
private:
    int cur{1}, prv{0};

public:
    Fibiter() = default;
    Fibiter &operator++()
    {
        prv = exchange(cur, cur + prv);

        return *this;
    }

    int operator*() { return cur; }
    auto operator<=>(const Fibiter &) const = default;
};

Fibiter begin(fibonacci) { return Fibiter{}; }
Fibiter end(fibonacci fib)
{
    Fibiter it;

    while (*it <= fib.num)
        ++it;

    return it;
}

int main()
{
    for (auto el : fibonacci{100})
        cout << el << ' ';
    cout << endl;

    for (auto it = begin(fibonacci{}); it != end(fibonacci{1000}); ++it)
        cout << *it << ' ';
    cout << endl;
}