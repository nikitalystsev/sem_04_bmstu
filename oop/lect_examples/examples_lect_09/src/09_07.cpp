// Пример 09.07. Концепты и перегрузка.
#include <iostream>
#include <vector>

template <typename T>
constexpr bool is_vector = false;
template <typename T>
constexpr bool is_vector<std::vector<T>> = true;
template <typename T>
concept Vec = is_vector<T>;

template <typename T>
constexpr bool is_pointer = false;
template <typename T>
constexpr bool is_pointer<T *> = true;
template <typename T>
concept Ptr = is_pointer<T>;

template <typename T>
void f(T)
{
    std::cout << "def" << std::endl;
}

template <Ptr T>
void f(T t)
{
    std::cout << "ptr" << std::endl;
    f(*t);
}

template <Vec T>
void f(T t)
{
    std::cout << "vec" << std::endl;
    f(t[0]);
}

int main()
{
    std::vector v{1};

    auto pv = &v;
    auto ppv = &pv;

    std::vector vv{{v}};
    std::vector vvv{{vv}};

    f(ppv);
    std::cout << std::endl;

    f(v);
    std::cout << std::endl;

    f(vvv);
}