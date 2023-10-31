// Пример 07.11. Перегрузка бинарных и унарных операторов.
#include <iostream>

using namespace std;

class Complex
{
private:
    double re, im;

public:
    Complex(double r = 0., double i = 0.) : re(r), im(i)
    {
        cout << "re = "<< r << endl;
        cout << "im = "<< i << endl;
    }

    Complex operator-() const { return Complex(-re, -im); }
    Complex operator-(const Complex &c) const { return Complex(re + c.re, im + c.im); }
    friend Complex operator+(const Complex &c1, const Complex &c2);

    friend ostream &operator<<(ostream &os, const Complex &c);
};

Complex operator+(const Complex &c1, const Complex &c2)
{
    return Complex(c1.re + c2.re, c1.im + c2.im);
}

ostream &operator<<(ostream &os, const Complex &c)
{
    return os << c.re << " + " << c.im << "i";
}

int main()
{
    Complex c1(1., 1.), c2(1., 2.), c3(2., 1.);

    Complex c4 = c1 + c2;
    cout << c4 << endl;

    Complex c5 = 5 + c3;
    cout << c5 << endl;

    // Complex c6 = 6 - c3; Error!!!

    Complex c7 = -c1;
    cout << c7 << endl;
}
