// Пример 10.16. Реализация addressof.
#include <iostream>

using namespace std;

class A
{
private:
    int a;

public:
    A *operator&() const noexcept = delete;
};

namespace my
{
    template <typename T>
    T *addressof(T &v)
    {
        return reinterpret_cast<T *>(&const_cast<char &>(reinterpret_cast<const char &>(v)));
    }
}

int main()
{
    A obj;

    //    cout << &obj << endl; // Error!

    hex(cout);
    cout << my::addressof<A>(obj) << endl;
}