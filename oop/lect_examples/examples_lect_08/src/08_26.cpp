// Пример 08.25. Шаблоны с переменным числом параметров значений.
#include <iostream>

using namespace std;

#define PRIM_1

#ifdef PRIM_1
template <size_t...>
constexpr size_t sum = 0;

template <size_t first, size_t... other>
constexpr size_t sum<first, other...> = first + sum<other...>;

#elif defined(PRIM_2)
template <size_t... Nms>
size_t sum()
{
    auto list = {Nms...};

    size_t sm = 0;
    for (auto elem : list)
        sm += elem;

    return sm;
}
#elif defined(PRIM_3)
template <typename... Ags>
void stub(Ags...)
{
}

template <size_t... Nms>
size_t sum()
{
    size_t sm = 0;
    stub(sm += Nms...);
    return sm;
}

#elif defined(PRIM_4)
template <size_t... Nms>
size_t sum()
{
    return (Nms + ...);
}

#endif

int main()
{
#ifdef PRIM_1
    cout << sum<1, 2, 3, 4, 5> << endl;
#else
    cout << sum<1, 2, 3, 4, 5>() << endl;
#endif
}
