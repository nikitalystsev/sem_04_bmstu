// Пример 10.15. Реализация forward.
#include <iostream>
#include <memory>

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

    template <typename T>
    constexpr T &&forward(remove_reference_t<T> &value) noexcept
    {
        return static_cast<T &&>(value);
    }

    template <typename T>
    constexpr T &&forward(remove_reference_t<T> &&value) noexcept
    {
        return static_cast<T &&>(value);
    }
}

template <typename T, typename... Args>
shared_ptr<T> create(Args &&...args)
{
    return shared_ptr<T>(new T(my::forward<Args>(args)...));
}

struct Person
{
    Person(const string &name) { cout << "copy constructor" << endl; }
    Person(string &&name) { cout << "move constructor" << endl; }
};

int main()
{
    shared_ptr<Person> p1 = create<Person>("Ok!!!");

    string nm("name");
    shared_ptr<Person> p2 = create<Person>(nm);
}
