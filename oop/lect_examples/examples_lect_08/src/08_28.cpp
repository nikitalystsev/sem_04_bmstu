// Пример 08.27. Шаблон класса с переменным числом параметров.Рекурсивная реализация кортежа.
#include <iostream>

using namespace std;

template <typename... Types>
class Tuple;

template <typename Head, typename... Tail>
class Tuple<Head, Tail...>
{
private:
    Head value;
    Tuple<Tail...> tail;

public:
    Tuple() = default;
    Tuple(const Head &v, const Tuple<Tail...> &t) : value(v), tail(t) {}
    Tuple(const Head &v, const Tail &...tail) : value(v), tail(tail...) {}

    Head &getHead() { return value; }
    const Head &getHead() const { return value; }

    Tuple<Tail...> &getTail() { return tail; }
    const Tuple<Tail...> &getTail() const { return tail; }
};

template <>
class Tuple<>
{
};

template <size_t N>
struct Get
{
    template <typename Head, typename... Tail>
    static auto apply(const Tuple<Head, Tail...> &t)
    {
        return Get<N - 1>::apply(t.getTail());
    }
};

template <>
struct Get<0>
{
    template <typename Head, typename... Tail>
    static const Head &apply(const Tuple<Head, Tail...> &t)
    {
        return t.getHead();
    }
};

template <size_t N, typename... Types>
auto get(const Tuple<Types...> &t)
{
    return Get<N>::apply(t);
}

size_t count(const Tuple<> &)
{
    return 0;
}

template <typename Head, typename... Tail>
size_t count(const Tuple<Head, Tail...> &t)
{
    return 1 + count(t.getTail());
}

ostream &writeTuple(ostream &os, const Tuple<> &)
{
    return os;
}

template <typename Head, typename... Tail>
ostream &writeTuple(ostream &os, const Tuple<Head, Tail...> &t)
{
    os << t.getHead() << " ";
    return writeTuple(os, t.getTail());
}

template <typename... Types>
ostream &operator<<(ostream &os, const Tuple<Types...> &t)
{
    return writeTuple(os, t);
}

int main()
{
    Tuple<const char *, double, int, char> obj("Pi: ", 3.14, 15, '!');

    cout << get<0>(obj) << get<1>(obj) << get<2>(obj) << get<3>(obj) << endl;

    cout << obj << endl;

    cout << "Count = " << count(obj) << endl;
}
