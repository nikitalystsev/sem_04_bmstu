// Пример 10.01. Использование итераторов для массива С и контенеров.
#include <iostream>

#include <vector>
#include <list>
#include <iterator>
#include <concepts>

using namespace std;

template <input_iterator Iter>
void print(Iter &&first, Iter &&last)
{
    for (auto it = first; it != last; ++it)
        cout << *it << ' ';
    cout << endl;
}

int main()
{
    int v1[]{1, 2, 3, 4, 5};

    cout << "iterator array: ";
    print(begin(v1), end(v1));

    vector v2{1, 2, 3, 4, 5};

    cout << "iterator vector: ";
    print(v2.begin(), v2.end());

    cout << "const iterator vector: ";
    print(v2.cbegin(), v2.cend());

    cout << "reverse_iterator vector: ";
    print(v2.rbegin(), v2.rend());

    cout << "const_reverse_iterator vector: ";
    print(v2.crbegin(), v2.crend());

    const vector v3{1, 2, 3, 4, 5};

    cout << "const_iterator vector: ";
    print(v3.begin(), v3.end());

    cout << "const_reverse_iterator: ";
    print(v3.rbegin(), v3.rend());

    list l{1, 2, 3, 4, 5};

    cout << "iterator list: ";
    print(l.begin(), l.end());
}