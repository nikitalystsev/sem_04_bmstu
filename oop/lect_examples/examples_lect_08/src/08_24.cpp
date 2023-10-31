// Пример 08.23. Использование sizeof.
#include <iostream>

using namespace std;

template <class... Ts>
pair<size_t, common_type_t<Ts...>> sum(Ts... params)
{
    return {sizeof...(Ts), (params + ...)};
}

int main()
{
    auto [iNumbers, iSum]{sum(1, 2, 3, 4, 5, 6)};

    cout << iNumbers << ' ' << iSum << endl;
}
