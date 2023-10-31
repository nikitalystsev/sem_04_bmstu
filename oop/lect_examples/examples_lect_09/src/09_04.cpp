// Пример 09.04. Концепты с составными ограничениями по типу выражений.
#include <iostream>

using namespace std;

#define PRIM_3

#ifdef PRIM_1
template <typename T, typename U, typename = void>
struct is_equal_comparable : false_type
{
};

template <typename T, typename U>
struct is_equal_comparable<T, U,
                           void_t<decltype(declval<T>() == declval<U>())>> : true_type
{
};

template <typename T, typename U>
    requires is_equal_comparable<T, U>::value
bool ch_equal(T &&lhs, U &&rhs)
{
    return lhs == rhs;
}

#elif defined(PRIM_2)
template <typename T, typename U>
    requires requires(T t, U u) { t == u; }
bool ch_equal(T &&lhs, U &&rhs)
{
    return lhs == rhs;
}

#elif defined(PRIM_3)
template <typename T, typename U>
concept WeaklyEquialityComparable = requires(T t, U u) {
    {
        t == u
    } -> convertible_to<bool>;
    {
        t != u
    } -> convertible_to<bool>;
};

template <typename T>
concept EquialityComparable = WeaklyEquialityComparable<T, T>;

template <typename T>
concept StrictTotallyOrdered = EquialityComparable<T> &&
                               requires(const remove_reference_t<T> &t1, const remove_reference_t<T> &t2) {
                                   {
                                       t1 < t2
                                   } -> convertible_to<bool>;
                                   {
                                       t1 > t2
                                   } -> convertible_to<bool>;
                               };

template <typename T, typename U>
    requires WeaklyEquialityComparable<T, U>
bool ch_equal(T &&lhs, U &&rhs)
{
    return (lhs <=> rhs) == 0;
}

#endif

int main()
{
    cout << boolalpha << ch_equal(3., 1) << endl;
    //    cout << ch_equal(" ", 1) << endl;
}