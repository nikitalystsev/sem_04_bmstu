// Пример 10.08. Диапазон из итераторов.
#include <iostream>
#include <vector>

using namespace std;

template <input_iterator Iter>
class Range
{
public:
    using value_type = Iter::value_type;
    using size_type = size_t;
    using iterator = Iter;
    using const_iterator = const Iter;

private:
    Iter first, last;

public:
    Range(Iter fst, Iter lst) : first(fst), last(lst) {}

    size_t size() const noexcept;

    iterator begin() { return first; }
    iterator end() { return last; }
};

template <input_iterator Iter>
size_t Range<Iter>::size() const noexcept
{
    return distance(first, last);
}

int main()
{
    vector v{1, 2, 3, 4, 5};

    Range range{v.begin(), v.end()};

    cout << "count = " << range.size() << "; elems: ";
    for (auto elem : range)
        cout << elem << " ";
    cout << endl;
}
