// Пример 07.16. Этот безумный С++ и оператор ->*.
#include <iostream>

using namespace std;

auto operator->*(pair<int, int> &pr, bool key) -> decltype(key ? pr.first : pr.second)
{
    return key ? pr.first : pr.second;
}

auto main() -> int
{
    pair t{1, 2};

    t->*true += 2;

    /*
    Затем, значения элементов пары извлекаются в переменные f и s с помощью структурировного присваивания:
    */
    auto [f, s]{t};

    cout << "pair{" << f << ", " << s << "}" << endl;
}
