// Пример 08.13. Использование decltype на примере шаблонного класса Complex.
#include <iostream>

using namespace std;

template <typename T>
class Complex
{
private:
    T real;
    T imag;

public:
    Complex(const T &r, const T &i) : real(r), imag(i) {}
    template <typename U>
    auto operator+(const Complex<U> &d) const;

    const T &getReal() const { return real; }
    const T &getImag() const { return imag; }
};

template <typename T>
template <typename U>
auto Complex<T>::operator+(const Complex<U> &d) const
{
    return Complex<decltype(real + d.getReal())>(real + d.getReal(), imag + d.getImag());
}

template <typename Type>
ostream &operator<<(ostream &os, const Complex<Type> &com)
{
    return os << "(" << com.getReal() << ", " << com.getImag() << ")" << endl;
}

int main()
{
    Complex c1(1.1, 2.2);
    Complex c2(1, 2);

    cout << c2 + c1 << endl;
}
