// Пример 13.22. .
#include <iostream>
#include <type_traits>
#include <tuple>

using namespace std;

namespace my
{
    const struct p_1_
    {
        static const unsigned index = 0;
    } _1_;
    const struct p_2_
    {
        static const unsigned index = 1;
    } _2_;
    const struct p_3_
    {
        static const unsigned index = 2;
    } _3_;

    template <typename T>
    concept PlaceHolder = is_same_v<T, p_1_> || is_same_v<T, p_2_> || is_same_v<T, p_3_>;

    template <typename T>
    concept NotPlaceHolder = !PlaceHolder<T>;

    template <PlaceHolder BindArg, typename CallArgTuple>
    auto get_arg(BindArg, CallArgTuple &&call_args)
    {
        return std::get<BindArg::index>(call_args);
    }

    template <NotPlaceHolder BindArg, typename CallArgTuple>
    auto get_arg(BindArg arg, CallArgTuple &&)
    {
        return arg;
    }

    template <typename F, typename... BindArgs>
    struct binder
    {
        F f;
        tuple<BindArgs...> bind_args;

        template <typename CallArgTuple, size_t... Indexes>
        auto call(std::index_sequence<Indexes...>, CallArgTuple &&call_args)
        {
            return f(get_arg(std::get<Indexes>(bind_args), call_args)...);
        }

        template <typename... CallArgs>
        auto operator()(CallArgs... call_args)
        {
            return call(std::make_index_sequence<sizeof...(BindArgs)>(), std::make_tuple(call_args...));
        }
    };

    template <typename F, typename... BindArgs>
    binder<F, BindArgs...> bind(F f, BindArgs... bind_args)
    {
        return {f, {bind_args...}};
    }
}

void foo(int a, int b)
{
    std::cout << a << " " << b << std::endl;
}

int main()
{
    auto f1 = my::bind(foo, 5, my::_1_);
    f1(8);

    auto f2 = my::bind(foo, my::_2_, my::_1_);
    f2(5, 8);

    auto f3 = my::bind(foo, 5, 8);
    f3();
}