// Пример 07.17. Перегрузка операторов [], =, ++ и приведения типа.
#include <iostream>
#include <exception>
#include <cstring>
#include <stdexcept>

using namespace std;

class Index
{
private:
    int ind;

public:
    Index(int i = 0) : ind(i) {}

    Index &operator++() // ++obj
    {
        ++ind;

        return *this;
    }
    Index operator++(int) // obj++
    {
        Index it(*this);
        ++ind;

        return it;
    }
    operator int() const { return ind; }
};

class Array
{
public:
    explicit Array(int n = 0) : cnt(n)
    {
        mas = cnt > 0 ? new double[cnt] : ((cnt = 0), nullptr);
    }
    explicit Array(const Array &arr) { copy(arr); }
    Array(Array &&arr) noexcept { move(arr); }
    ~Array() { delete[] mas; }

    Array &operator=(const Array &arr);
    Array &operator=(Array &&arr) noexcept;

    double &operator[](const Index &index);
    const double &operator[](const Index &index) const;

    int count() const { return cnt; }

private:
    double *mas;
    int cnt;

    void copy(const Array &arr);
    void move(Array &arr) noexcept;
};

Array &Array::operator=(const Array &arr)
{
    if (this == &arr)
        return *this;

    delete[] mas;

    copy(arr);

    return *this;
}

Array &Array::operator=(Array &&arr) noexcept
{
    delete[] mas;

    move(arr);

    return *this;
}

double &Array::operator[](const Index &index)
{
    if (index < 0 || index >= cnt)
        throw std::out_of_range("Error: class Array operator [];");

    return mas[index];
}

const double &Array::operator[](const Index &index) const
{
    if (index < 0 || index >= cnt)
        throw std::out_of_range("Error: class Array operator [];");

    return mas[index];
}

void Array::copy(const Array &arr)
{
    cnt = arr.cnt;
    mas = new double[cnt];
    memcpy(mas, arr.mas, cnt * sizeof(double));
}

void Array::move(Array &arr) noexcept
{
    cnt = arr.cnt;
    mas = arr.mas;
    arr.mas = nullptr;
}

Array operator*(const Array &arr, double d)
{
    Array a(arr.count());

    for (Index i; i < arr.count(); i++)
        a[i] = d * arr[i];

    return a;
}

Array operator*(double d, const Array &arr) { return arr * d; }

Array operator+(const Array &arr1, const Array &arr2)
{
    if (arr1.count() != arr2.count())
        throw std::length_error("Error: operator +;");

    Array a(arr1.count());

    for (Index i; i < arr1.count(); i++)
        a[i] = arr1[i] + arr2[i];

    return a;
}

istream &operator>>(istream &is, Array &arr)
{
    for (Index i; i < arr.count(); i++)
        cin >> arr[i];

    return is;
}

ostream &operator<<(ostream &os, const Array &arr)
{
    for (Index i; i < arr.count(); i++)
        cout << " " << arr[i];

    return os;
}

int main()
{
    try
    {
        const int N = 3;
        Array a1(N), a2;

        cout << "Input of massive (size = " << a1.count() << "): ";
        cin >> a1;

        // a2 = a1 + 5; Error!!!
        a2 = 2 * a1;

        cout << "Result: " << a2 << endl;
    }
    catch (const std::exception &exc)
    {
        cout << exc.what() << endl;
    }
}