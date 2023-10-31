// Пример 10.14. Реализация move.
#include <iostream>

using namespace std;

namespace my
{
    template <typename T>
    struct remove_reference
    {
        using type = T;
    };
    template <typename T>
    struct remove_reference<T &>
    {
        using type = T;
    };
    template <typename T>
    struct remove_reference<T &&>
    {
        using type = T;
    };

    template <typename T>
    using remove_reference_t = typename remove_reference<T>::type;

#define V_1

#ifdef V_1
    template <typename T>
    typename remove_reference<T>::type &&move(T &&t)
    {
        return static_cast<typename remove_reference<T>::type &&>(t);
    }

#elif defined(V_2)
    template <typename T>
    remove_reference_t<T> &&move(T &&t)
    {
        return static_cast<remove_reference_t<T> &&>(t);
    }

#elif defined(V_3)
    decltype(auto) move(auto &&t)
    {
        return static_cast<remove_reference_t<decltype(t)> &&>(t);
    }

#endif
}

class A
{
public:
    A() { cout << "constructor" << endl; }
    A(const A &over) { cout << "copy constructor" << endl; }
    A(A &&over) noexcept { cout << "move constructor" << endl; }
    ~A() { cout << "destructor" << endl; }

    A &operator=(const A &over)
    {
        cout << "copy assignment operator" << endl;
        return *this;
    }
    A &operator=(A &&over) noexcept
    {
        cout << "move assignment operator" << endl;
        return *this;
    }
};

template <typename Type>
void mySwap(Type &d1, Type &d2)
{
    Type dt = my::move(d1);
    d1 = my::move(d2);
    d2 = my::move(dt);
}

int main()
{
    A obj1, obj2;

    mySwap(obj1, obj2);
}