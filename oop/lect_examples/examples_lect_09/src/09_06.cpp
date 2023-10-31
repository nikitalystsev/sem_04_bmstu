// Пример 09.06. Концепт с вариативным количеством параметров.
#include <iostream>
#include <concepts>

using namespace std;

template <typename Type, typename... Types>
constexpr inline bool are_same_v = conjunction_v<is_same<Type, Types>...>;

#define PRIM_3

#ifdef PRIM_1
template <typename Type, typename... Types>
    requires(is_same_v<Type, Types> && ... && true)
auto sum(Type &&value, Types &&...params)
{
    return forward<Type>(value) + (... + forward<Types>(params));
}

#elif defined(PRIM_2)
template <typename... Types>
    requires are_same_v<Types...>
auto sum(Types &&...params)
{
    return (... + forward<Types>(params));
}

#elif defined(PRIM_3)
template <typename Type, typename... Types>
struct first_arg
{
    using type = Type;
};

template <typename... Types>
using first_arg_t = typename first_arg<Types...>::type;

template <typename... Types>
concept Addable = requires(Types &&...args) {
    {
        (... + forward<Types>(args))
    } -> same_as<first_arg_t<Types...>>;

    requires are_same_v<Types...>;
    requires sizeof...(Types) > 1;
};

template <typename... Types>
    requires Addable<Types...>
auto sum(Types &&...args)
{
    return (... + forward<Types>(args));
}

#endif

int main()
{
    cout << sum(1., 2., 3., 4., 5.) << endl;
}