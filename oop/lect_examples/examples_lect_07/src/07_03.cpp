// Пример 07.03. Try и Catch блоки уровня методов.
#include <iostream>
#include <exception>

using namespace std;

class A
{
public:
    void f(int v);
};

void A::f(int v)
try
{
    if (v < 0)
        throw std::runtime_error("error in method f!");
}
catch (const std::runtime_error &err)
{
    cout << err.what() << " v = " << v << endl;
}

int main()
{
    A obj;

    obj.f(-1);

    return 0;
}