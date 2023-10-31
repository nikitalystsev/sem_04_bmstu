// Пример 09.05. Использование концепта с несколькими параметрами.
#include <iostream>

using namespace std;

template <typename BI, typename EI>
concept Comparable = requires(BI bi, EI ei) {
    {
        bi == ei
    } -> convertible_to<bool>;
};

#define VARIANT_3

#ifdef VARIANT_1
template <typename EI, Comparable<EI> BI>
constexpr bool my_equal(BI bi, EI ei)
{
    return bi == ei;
}

#elif defined(VARIANT_2)
template <typename BI, typename EI>
    requires Comparable<BI, EI>
constexpr bool my_equal(BI bi, EI ei)
{
    return bi == ei;
}

#elif defined(VARIANT_3)
template <typename BI, typename EI>
constexpr bool my_equal(BI bi, EI ei)
    requires Comparable<BI, EI>
{
    return bi == ei;
}

#endif

class A
{
public:
    bool operator==(const A &) { return true; }
};

class B
{
public:
    operator A() { return A{}; }
};

int main()
{
    cout << boolalpha << my_equal(1., 1) << endl;

    A objA{};
    B objB{};

    cout << boolalpha << my_equal(objA, objB) << endl;
}