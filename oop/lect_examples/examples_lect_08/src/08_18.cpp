// Пример 08.17. Частичная специализация шаблона класса, параметры шаблона класса по умолчанию.
#include <iostream>

using namespace std;

template <typename T1, typename T2 = double>
class A
{
public:
    A() { cout << "constructor of template A<T1, T2>;" << endl; }
};

// Specialization #1
template <typename T>
class A<T, T>
{
public:
    A() { cout << "constructor of template A<T, T>;" << endl; }
};

// Specialization #2
template <typename T>
class A<T, int>
{
public:
    A() { cout << "constructor of template A<T, int>;" << endl; }
};

// Specialization #3
template <typename T1, typename T2>
class A<T1 *, T2 *>
{
public:
    A() { cout << "constructor of template A<T1*, T2*>;" << endl; }
};

int main()
{
    A<int> a0;            // Template
    A<int, float> a1;     // Template
    A<float, float> a2;   // Specialization #1
    A<float, int> a3;     // Specialization #2
    A<int *, float *> a4; // Specialization #3

    // A<int, int> a5;// Error!!!
    // A<int*, int*> a6;// Error!!!
}
