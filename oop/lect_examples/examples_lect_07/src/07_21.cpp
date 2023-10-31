// Пример 07.21. Перегрузка операторов на примере класс Array.
#include <iostream>
#include <initializer_list>
#include <exception>
#include <cstring>
#include <stdexcept>

using namespace std;

class Array final
{
public:
    explicit Array(int n = 0, double *a = nullptr);
    explicit Array(const Array &arr) { copy(arr.mas, arr.cnt); }
    Array(Array &&arr) noexcept { move(arr); }
    Array(initializer_list<double> list) { copy(list); }
    ~Array() { delete[] mas; }

    Array &operator=(const Array &arr);
    Array &operator=(Array &&arr) noexcept;
    Array &operator=(initializer_list<double> list);

    double &operator[](int index);
    const double &operator[](int index) const;

    explicit operator int() const { return cnt; }
    int count() const { return cnt; }

    Array &operator/=(double d);
    Array operator/(double d) const;

    Array &operator*=(double d);
    Array operator*(double d) const;

    Array operator-() const;

    Array &operator-=(const Array &arr);
    Array &operator-=(initializer_list<double> list);
    Array operator-(const Array &arr) const;

private:
    double *mas;
    int cnt;

    void copy(const double *a, int n);
    void copy(initializer_list<double> list);
    void move(Array &arr) noexcept;
};

Array operator*(double d, const Array &arr);

#pragma region Methods Array
Array::Array(int n, double *a)
{
    if (n <= 0)
    {
        cnt = 0;
        mas = nullptr;
    }
    else
    {
        copy(a, n);
    }
}

Array &Array::operator=(const Array &arr)
{
    if (this == &arr)
        return *this;

    delete[] mas;

    copy(arr.mas, arr.cnt);

    return *this;
}

Array &Array::operator=(Array &&arr) noexcept
{
    delete[] mas;

    move(arr);

    return *this;
}

Array &Array::operator=(initializer_list<double> list)
{
    delete[] mas;

    copy(list);

    return *this;
}

double &Array::operator[](int index)
{
    if (index < 0 || index >= cnt)
        throw std::out_of_range("Error: class Array operator [];");

    return mas[index];
}

const double &Array::operator[](int index) const
{
    if (index < 0 || index >= cnt)
        throw std::out_of_range("Error: class Array operator [];");

    return mas[index];
}

void Array::copy(const double *a, int n)
{
    cnt = n;
    mas = new double[cnt];
    if (a)
    {
        memcpy(mas, a, cnt * sizeof(double));
    }
}

void Array::copy(initializer_list<double> list)
{
    cnt = list.size();
    mas = new double[cnt];

    for (int i = 0; auto elem : list)
        mas[i++] = elem;
}

void Array::move(Array &arr) noexcept
{
    cnt = arr.cnt;
    mas = arr.mas;
    arr.mas = nullptr;
}

Array &Array::operator/=(double d)
{
    if (d == 0.)
        throw std::invalid_argument("Error: divide by zero;");

    for (int i = 0; i < cnt; i++)
        mas[i] /= d;

    return *this;
}

Array Array::operator/(double d) const
{
    Array a(*this);

    a /= d;

    return a;
}

Array &Array::operator*=(double d)
{
    for (int i = 0; i < cnt; i++)
        mas[i] *= d;

    return *this;
}

Array Array::operator*(double d) const
{
    Array a(*this);

    a *= d;

    return a;
}

Array Array::operator-() const
{
    return -1. * (*this);
}

Array &Array::operator-=(const Array &arr)
{
    if (cnt != arr.cnt)
        throw std::length_error("Error: operator -;");

    for (int i = 0; i < cnt; i++)
        mas[i] -= arr[i];

    return *this;
}

Array &Array::operator-=(initializer_list<double> list)
{
    if (cnt != list.size())
        throw std::length_error("Error: operator -;");

    for (int i = 0; auto elem : list)
        mas[i++] -= elem;

    return *this;
}

Array Array::operator-(const Array &arr) const
{
    Array a(*this);

    a -= arr;

    return a;
}

#pragma endregion

Array operator*(double d, const Array &arr)
{
    return arr * d;
}

istream &operator>>(istream &is, Array &arr)
{
    for (int i = 0; i < arr.count(); i++)
        is >> arr[i];

    return is;
}

ostream &operator<<(ostream &os, const Array &arr)
{
    for (int i = 0; i < arr.count(); i++)
        os << " " << arr[i];

    return os;
}

int main()
{
    try
    {
        const int N = 3;
        Array a1(N), a2, a4{2., 4., 6.};

        cout << "Input of massive (size = " << a1.count() << "): ";
        cin >> a1;
        cout << "Result a1: " << a1 << endl;

        a2 = 2. * a1;
        cout << "Result a2: " << a2 << endl;

        Array a3 = -a1;
        cout << "Result a3: " << a3 << endl;

        a4 -= {3., 2., 1.};
        cout << "Result a4: " << a4 << endl;

        Array a5 = a2 - a3;
        cout << "Result a5: " << a5 << endl;
    }
    catch (const exception &exc)
    {
        cout << exc.what() << endl;
    }
}