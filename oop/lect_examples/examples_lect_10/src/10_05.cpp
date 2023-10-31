// Пример 10.05. Реализация copy.
#include <iostream>
#include <concepts>
#include <list>
#include <vector>
#include <iterator>

using namespace std;

namespace my
{
    template <input_iterator InputIt,
              output_iterator<typename iterator_traits<InputIt>::value_type> OutputIt>
    auto copy(InputIt first, InputIt last, OutputIt dfirst)
    {
        for (auto it = first; it != last; ++it, ++dfirst)
            *dfirst = *it;

        return dfirst;
    }
}

int main()
{
    list l{1, 2, 3, 4, 5};

    vector<int> v;

    my::copy(l.begin(), l.end(), std::back_inserter(v));

    my::copy(v.begin(), v.end(), ostream_iterator<int>(cout, " "));
}