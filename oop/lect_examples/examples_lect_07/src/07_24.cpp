// Пример 07.24. Варианты перегрузки оператора “space ship”.
#include <iostream>
#include <compare>

using namespace std;

class MyInt
{
private:
    int value;

public:
    MyInt(int val = 0) : value(val) {}

    // strong_ordering operator <=>(const MyInt& rhs) const
    //{
    //     return value <=> rhs.value;
    // }

    // strong_ordering operator <=>(const MyInt& rhs) const
    //{
    //     return value == rhs.value ? strong_ordering::equal :
    //             value < rhs.value ? strong_ordering::less :
    //                                 strong_ordering::greater;
    // }

    // weak_ordering operator <=>(const MyInt& rhs) const
    //{
    //     return value == rhs.value ? weak_ordering::equivalent :
    //             value < rhs.value ? weak_ordering::less :
    //                                 weak_ordering::greater;
    // }

    partial_ordering operator<=>(const MyInt &rhs) const
    {
        return value == rhs.value ? partial_ordering::equivalent : value < rhs.value ? partial_ordering::less
                                                               : value > rhs.value   ? partial_ordering::greater
                                                                                     : partial_ordering::unordered;
    }

    bool operator==(const MyInt &) const = default;
};

int main()
{
    MyInt a{1}, b{2}, c{3}, d{1};
    cout << "a < b: " << (a < b) << ", c > b: " << (c >= b) << endl;
    cout << "a < b: " << (a < b) << ", c > b: " << (c > b) << ", a != b: " << (a != b) << endl;
    cout << "a < 5: " << (a < 5) << ", 1 < c: " << (1 < c) << endl;
}