// Пример 07.19. Оператор new для массива.
#include <iostream>

using namespace std;

class Complex
{
    double re, im;

public:
    Complex(double r = 0., double i = 0.) : re(r), im(i) {}

    double getR() const { return re; }
    double getI() const { return im; }
};

ostream &operator<<(ostream &os, const Complex &c)
{
    return os << " ( " << c.getR() << ", " << c.getI() << " )";
}

int main()
{
    const int count = 10;
    Complex *arr = new Complex[count]{1., {2., 3.}, Complex(4., 5.), 6., 7.};

    for (int i = 0; i < count; i++)
        cout << arr[i];
    cout << endl;

    delete[] arr;
}