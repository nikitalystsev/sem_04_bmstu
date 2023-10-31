// Пример 08.08. Конструктор для вывода типа параметра шаблона класса.
#include <iostream>

using namespace std;

template <typename Type>
class Complex
{
private:
    Type re, im;

public:
    Complex(Type r, Type i) : re(r), im(i) {}

    Type getReal() const { return re; }
    Type getImage() const { return im; }
};

template <typename Type>
ostream &operator<<(ostream &os, const Complex<Type> &c)
{
    return os << "(" << c.getReal() << "; " << c.getImage() << ")";
}

int main()
{
    Complex c(1., 2.);

    cout << c << endl;
}