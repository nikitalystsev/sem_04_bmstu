// Пример 08.29. Выведение типа и стирание ссылок и const.
#include <iostream>

#define V_1

#ifdef V_1
template <typename T>
T f(T v)
{
    return v;
}

#elif defined(V_2)
template <typename T>
T f(T &v)
{
    return v;
}

#elif defined(V_3)
template <typename T>
T f(const T &v)
{
    return v;
}

#elif defined(V_4)
template <typename T>
T f(T &&v)
{
    return v;
}

#elif defined(V_5)
template <typename T>
T &f(T &&v)
{
    return v;
}

#elif defined(V_6)
template <typename T>
T &&f(T &&v)
{
    return std::forward<T>(v);
}

#elif defined(V_7)
auto f(auto v)
{
    return v;
}

#elif defined(V_8)
auto f(auto &v)
{
    return v;
}

#elif defined(V_9)
auto f(const auto &v)
{
    return v;
}

#elif defined(V_10)
auto &&
f(auto &&v)
{
    return v;
}

#elif defined(V_11)
auto &&
f(auto &&v)
{
    return std::forward<decltype(v)>(v);
}

#elif defined(V_12)
decltype(auto)
f(auto &&v)
{
    return std::forward<decltype(v)>(v);
}

#elif defined(V_13)
template <typename T>
auto f(T &&v) -> decltype(v)
{
    return std::forward<T>(v);
}

#endif

int main()
{
    int i;
    int &a = i;
    const int &b = 0;

    decltype(auto) r1 = f(i);
    // 1. T f(T v)--->int f<int>(int)
    // 2. T f(T& v)--->int f<int>(int&)
    // 3. T f(const T& v)--->int f<int>(const int&)
    // 4. T f(T&& v)--->int& f<int&>(int&)
    // 5. T& f(T&& v)--->int& f<int&>(int&)
    // 6. T&& f(T&& v) { return std::forward<T>(v); }--->int& f<int&>(int&)
    // 7. auto f(auto v)--->int f<int>(int)
    // 8. auto f(auto& v)--->int f<int>(int&)
    // 9. auto f(const auto& v)--->int f<int>(const int&)
    // 10. auto&& f(auto&& v)--->int& f<int&>(int&)
    // 11. auto&& f(auto&& v) { return std::forward<decltype(v)>(v); }
    // --->int& f<int&>(int&)
    // 12. decltype(auto) f(auto&& v) { return std::forward<decltype(v)>(v); }
    // --->int& f<int&>(int&)
    // 13. auto f(T&& v) -> decltype(v) { return std::forward<T>(v); }
    //--->int& f<int&>(int&)

    decltype(auto) r2 = f(a);
    // 1. T f(T v)--->int f<int>(int)
    // 2. T f(T& v)--->int f<int>(int&)
    // 3. T f(const T& v)--->int f<int>(const int&)
    // 4. T f(T&& v)--->int& f<int&>(int&)
    // 5. T& f(T&& v)--->int& f<int&>(int&)
    // 6. T&& f(T&& v) { return std::forward<T>(v); }--->int& f<int&>(int&)
    // 7. auto f(auto v)--->int f<int>(int)
    // 8. auto f(auto& v)--->int f<int>(int&)
    // 9. auto f(const auto& v)--->int f<int>(const int&)
    // 10. auto&& f(auto&& v)--->int& f<int&>(int&)
    // 11. auto&& f(auto&& v) { return std::forward<decltype(v)>(v); }
    // --->int& f<int&>(int&)
    // 12. decltype(auto) f(auto&& v) { return std::forward<decltype(v)>(v); }
    // --->int& f<int&>(int&)
    // 13. auto f(T&& v) -> decltype(v) { return std::forward<T>(v); }
    //--->int& f<int&>(int&)

    decltype(auto) r3 = f(b);
    // 1. T f(T v)--->int f<int>(int)
    // 2. T f(T& v)--->const int f<const int>(const int&)
    // 3. T f(const T& v)--->int f<int>(const int&)
    // 4. T f(T&& v)--->const int& f<const int&>(const int&)
    // 5. T& f(T&& v)--->const int& f<const int&>(const int&)
    // 6. T&& f(T&& v) { return std::forward<T>(v); }
    // --->const int& f<const int&>(const int&)
    // 7. auto f(auto v)--->int f<int>(int)
    // 8. auto f(auto& v)--->int f<const int>(const int&)
    // 9. auto f(const auto& v)--->int f<int>(const int&)
    // 10. auto&& f(auto&& v)--->const int& f<const int&>(const int&)
    // 11. auto&& f(auto&& v) { return std::forward<decltype(v)>(v); }
    // --->const int& f<const int&>(const int&)
    // 12. decltype(auto) f(auto&& v) { return std::forward<decltype(v)>(v); }
    // --->const int& f<const int&>(const int&)
    // 13. auto f(T&& v) -> decltype(v) { return std::forward<T>(v); }
    //--->const int& f<const int&>(const int&)

    decltype(auto) r4 = f(std::move(a));
    // 1. T f(T v)--->int f<int>(int)
    // 2. T f(T& v)--->Error!
    // 3. T f(const T& v)--->int f<int>(const int&)
    // 4. T f(T&& v)--->int f<int>(int) // вопрос!
    // 5. T& f(T&& v)--->int& f<int>(int&&)
    // 6. T&& f(T&& v) { return std::forward<T>(v); }--->int&& f<int>(int&&)
    // 7. auto f(auto v)--->int f<int>(int)
    // 8. auto f(auto& v)--->Error!
    // 9. auto f(const auto& v)--->int f<int>(const int&)
    // 10. auto&& f(auto&& v)--->int f<int>(int&&)
    // 11. auto&& f(auto&& v) { return std::forward<decltype(v)>(v); }
    // --->int&& f<int>(int&&)
    // 12. decltype(auto) f(auto&& v) { return std::forward<decltype(v)>(v); }
    // --->int&& f<int>(int&&)
    // 13. auto f(T&& v) -> decltype(v) { return std::forward<T>(v); }
    //--->int&& f<int>(int&&)
}