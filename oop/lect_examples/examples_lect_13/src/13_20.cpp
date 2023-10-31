// Пример 13.20. “Статический полиморфизм”. MixIn в виде свободного оператора.
#include <iostream>

using namespace std;

#pragma region Comparisons
template <typename Derived>
struct Comparisons
{
};

template <typename Derived>
bool operator==(const Comparisons<Derived> &c1, const Comparisons<Derived> &c2)
{
    const Derived &d1 = static_cast<const Derived &>(c1);
    const Derived &d2 = static_cast<const Derived &>(c2);

    return !(d1 < d2) && !(d2 < d1);
}

template <typename Derived>
bool operator!=(const Comparisons<Derived> &c1, const Comparisons<Derived> &c2)
{
    return !(c1 == c2);
}

#pragma endregion

#pragma region Object_t
template <typename Derived>
struct Object_t
{
public:
    virtual ~Object_t() = default;

    bool less(const Object_t<Derived> &rhs) const
    {
        const Derived &rs = static_cast<const Derived &>(rhs);

        return static_cast<const Derived *>(this)->less(rs);
    }

protected:
    Object_t() = default;
};

template <typename Derived>
bool operator<(const Object_t<Derived> &lhs, const Object_t<Derived> &rhs)
{
    return lhs.less(rhs);
}

#pragma endregion

class Int_t : public Object_t<Int_t>, public Comparisons<Int_t>
{
public:
    Int_t() : Int_t(0) {}
    Int_t(int d) : data(d) {}

    bool less(const Int_t &rhs) const { return data < rhs.data; }

private:
    int data;
};

int main()
{
    Int_t i{10}, j{10}, k;

    if (i == j)
        cout << "i == j" << endl;
    else
        cout << "i != j" << endl;

    Object_t<Int_t> &ref = k;

    cout << boolalpha << ref.less(j) << endl;
}
