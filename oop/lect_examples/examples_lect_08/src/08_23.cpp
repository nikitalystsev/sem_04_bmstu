// Пример 08.22. Использование вариативных выражений.
#include <iostream>
#include <cmath>

using namespace std;

template <typename... Ts>
auto sum(Ts... params)
{
    return (params + ...);
}

template <typename... Ts>
auto length(Ts... params)
{
    return sqrt(sum(params * params...));
}

int main()
{
    cout << length(1., 2., 3., 4., 5.) << endl;
}