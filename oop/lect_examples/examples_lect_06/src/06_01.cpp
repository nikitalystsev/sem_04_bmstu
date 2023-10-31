// Пример 06.01. Инициализация объектов.
#include <iostream>
#include <initializer_list>

using namespace std;

class Complex
{
private:
    double _re, _im;

public:
    // explicit
    Complex() = default;
    // explicit
    Complex(double r) : Complex(r, 0.) {}
    Complex(int r) : Complex(r, 0.) {}
    // explicit
    Complex(double r, double i) : _re(r), _im(i) {}
    // explicit
    Complex(const Complex &C) : Complex(C._re, C._im) {}
    Complex(Complex &&C) : Complex(C._re, C._im) {}

    // explicit
    Complex(initializer_list<double> list)
    {
        for (double elem : list)
        {
        }
        // for (const double* p = list.begin(); p != list.end(); p++) {}
    }

    void set_Real(int r) { this->_re = r; }
    void set_Real(double) = delete;

    static Complex sum(const Complex &c1, const Complex &c2)
    {
        Complex ctmp(c1._re + c2._re, c1._im + c2._im);

        return ctmp;
    }

    Complex &operator=(const Complex &c)
    {
        this->_re = c._re;
        this->_im = c._im;

        return *this;
    }

    Complex &operator=(Complex &&c)
    {
        this->_re = c._re;
        this->_im = c._im;

        return *this;
    }
    /*
    Complex& operator=(initializer_list<double> list)
    {
    return *this;
    }
    */
};

int main()
{
    Complex a1(),        // объявление функции
        a2(Complex()),   // объявление функции
        b1,              // явный вызов Complex()
        b2{},            // явный вызов Complex(). инициализация 0
        b3 = {},         // неявный вызов Complex(). инициализация 0
        b4((Complex())), // явный вызов Complex(). инициализация 0
        b5(Complex{}),   // явный вызов Complex(). инициализация 0
        b6 = Complex{},  // явный вызов Complex(). инициализация 0

        c1_1(1.5), c1_2(1), // явный вызов Complex(double), Complex(int)
        c2 = Complex(5.5),  // явный вызов Complex(double)
        c3{2.},             // явный вызов Complex(double) | Complex(initializer_list)
        c4 = {3.},          // неявный вызов Complex(double) | Complex(initializer_list)
        c5 = Complex({4.}), // явный вызов Complex(double) | Complex(initializer_list)
        c6 = 4.5,           // неявный вызов Complex(double)

        d1(1., 2.),           // явный вызов Complex(double, double)
        d4 = Complex(4., 5.), // явный вызов Complex(double, double)
        d2{2., 3.},           // Complex(double, double) | Complex(initializer_list)
        d3 = {3., 4.},        // неявный вызов
        // Complex(double, double) | Complex(initializer_list)
        d5 = Complex({5., 6.}), // неявный вызов
        // Complex(double, double) | Complex(initializer_list)

        e1(c1_1),           // явный вызов Complex(const Complex&)
        e2 = Complex(c2),   // явный вызов Complex(const Complex&)
        e3{c3},             // явный вызов Complex(const Complex&)
        e4 = {c4},          // неявный вызов Complex(const Complex&)
        e5 = Complex({c5}), // неявный вызов Complex(const Complex&)
        e6 = c6,            // неявный вызов Complex(const Complex&)

        f1(Complex::sum(c1_1, c2)); // вызов Complex(Complex&&)

    b1 = {}; // неявный вызов ( Complex() & operator=(Complex&&) )
    // | operator=(initializer_list)
    b2 = Complex{}; // явный вызов Complex() & operator=(Complex&&)
    c1_1 = {1.};    // неявный вызов ( Complex(double) & operator=(Complex&&) )
    // | ( Complex(initializer_list) & operator=(Complex&&) )
    // | operator=(initializer_list)
    c4 = 4.;       // неявный вызов Complex(double) & operator=(Complex&&)
    d1 = {2., 3.}; // неявный вызов ( Complex(double, double) & operator=(Complex&&) )
    // | ( Complex(initializer_list) & operator=(Complex&&) )
    // | operator=(initializer_list)

    e1.set_Real(1); // '1', 1l, L'1' - Ok! 1ll, 1u, 1lu, 1.f, 1.l, "1" - Error!

    return 0;
}