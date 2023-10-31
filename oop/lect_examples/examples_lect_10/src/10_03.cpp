// Пример 10.03. Пример вложенного итератора.
#include <iostream>
#include <iterator>

using namespace std;

/*
template <
    typename Category,                  // категория итератора
    typename T,                         // тип значения
    typename Distance = ptrdiff_t,      // тип расстояния между итераторами
    typename Pointer = T*,              // указатель на значение
    typename Reference = T&             // ссылка на значение
> struct iterator;
*/

template <int FROM, int TO>
class Range
{
public:
    class iterator
    {
    private:
        int num = FROM;

    public:
        using iterator_category = input_iterator_tag;

        using value_type = int;
        using difference_type = int;
        using pointer = const int *;
        using reference = const int &;

        explicit iterator(long nm = 0) : num(nm) {}
        iterator &operator++()
        {
            num += FROM <= TO ? 1 : -1;
            return *this;
        }
        iterator operator++(int)
        {
            iterator retval = *this;
            ++(*this);
            return retval;
        }
        bool operator==(iterator other) const { return num == other.num; }
        bool operator!=(iterator other) const { return !(*this == other); }
        reference operator*() const { return num; }
    };

    iterator begin() { return iterator(FROM); }
    iterator end() { return iterator(FROM <= TO ? TO + 1 : TO - 1); }
};

int main()
{
    auto rng = Range<15, 25>();

    cout << "count elem = " << distance(rng.begin(), rng.end()) << endl;

    for (auto it = find(rng.begin(), rng.end(), 20); it != rng.end(); ++it)
    {
        cout << *it << ' ';
    }
    cout << endl;

    for (auto i : Range<5, 2>())
    {
        cout << i << ' ';
    }
    cout << endl;
}